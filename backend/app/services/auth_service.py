"""
认证服务层
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from jose import JWTError

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
)
from app.core.config import settings


class AuthenticationError(Exception):
    """认证异常"""
    pass


class UserAlreadyExistsError(Exception):
    """用户已存在异常"""
    pass


def register_user(
    db: Session,
    email: str,
    password: str,
    full_name: Optional[str] = None
) -> User:
    """
    注册新用户

    Args:
        db: 数据库会话
        email: 邮箱地址
        password: 明文密码
        full_name: 用户全名(可选)

    Returns:
        创建的用户对象

    Raises:
        UserAlreadyExistsError: 邮箱已被注册
    """
    # 检查邮箱是否已存在
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise UserAlreadyExistsError(f"邮箱 {email} 已被注册")

    # 创建新用户
    hashed_pw = hash_password(password)
    new_user = User(
        email=email,
        hashed_password=hashed_pw,
        full_name=full_name,
        credits=10,  # 新用户赠送10积分
        is_active=True,
        is_verified=False,  # 邮箱验证功能后续实现
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsError(f"邮箱 {email} 已被注册")


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    验证用户邮箱和密码

    Args:
        db: 数据库会话
        email: 邮箱地址
        password: 明文密码

    Returns:
        验证成功返回用户对象,失败返回 None
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    # OAuth 用户没有密码
    if not user.hashed_password:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    db.commit()

    return user


def create_tokens(user_id: str, email: str) -> dict:
    """
    为用户创建 access token 和 refresh token

    Args:
        user_id: 用户 ID
        email: 用户邮箱

    Returns:
        包含 access_token 和 refresh_token 的字典
    """
    token_data = {"sub": user_id, "email": email}

    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data=token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def verify_refresh_token(db: Session, refresh_token: str) -> Optional[User]:
    """
    验证 refresh token 并返回用户

    Args:
        db: 数据库会话
        refresh_token: JWT refresh token

    Returns:
        验证成功返回用户对象,失败返回 None
    """
    try:
        payload = decode_access_token(refresh_token)

        # 检查 token 类型
        if payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        user = db.query(User).filter(User.id == user_id).first()
        return user

    except JWTError:
        return None


def get_or_create_google_user(
    db: Session,
    google_id: str,
    email: str,
    full_name: Optional[str] = None
) -> User:
    """
    根据 Google OAuth 信息获取或创建用户

    Args:
        db: 数据库会话
        google_id: Google 用户 ID
        email: 邮箱地址
        full_name: 用户全名(可选)

    Returns:
        用户对象
    """
    # 先尝试通过 Google ID 查找
    user = db.query(User).filter(User.authentik_user_id == google_id).first()
    if user:
        # 更新最后登录时间
        user.last_login_at = datetime.utcnow()
        db.commit()
        return user

    # 再尝试通过邮箱查找
    user = db.query(User).filter(User.email == email).first()
    if user:
        # 关联 Google ID
        user.authentik_user_id = google_id
        user.last_login_at = datetime.utcnow()
        db.commit()
        return user

    # 创建新用户
    new_user = User(
        email=email,
        full_name=full_name,
        authentik_user_id=google_id,
        hashed_password=None,  # OAuth 用户没有密码
        credits=10,  # 新用户赠送10积分
        is_active=True,
        is_verified=True,  # Google 用户默认已验证
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
