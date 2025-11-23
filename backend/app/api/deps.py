"""
API 依赖项
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.supabase import supabase_jwt_verifier
from app.models.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户 - 使用 Supabase JWT 验证

    Args:
        credentials: HTTP Bearer Token (Supabase JWT)
        db: 数据库会话

    Returns:
        当前用户对象

    Raises:
        HTTPException: 认证失败时抛出 401
    """
    import logging
    logger = logging.getLogger(__name__)

    # 验证 Supabase JWT
    payload = supabase_jwt_verifier.verify_token(credentials.credentials)

    # 获取 Supabase 用户 ID
    supabase_user_id: str = payload.get("sub")
    logger.info(f"get_current_user - Supabase ID: {supabase_user_id}")

    if not supabase_user_id:
        logger.warning("Token 中缺少用户 ID")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 中缺少用户 ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 查询用户（通过 supabase_user_id）
    user = db.query(User).filter(User.supabase_user_id == supabase_user_id).first()
    logger.info(f"查询用户结果 - User: {user}")
    if user:
        logger.info(f"用户详情 - ID: {user.id}, Email: {user.email}, is_active: {user.is_active}, supabase_user_id: {user.supabase_user_id}")

    # 如果用户不存在，要求前端先调用 sync-user
    if user is None:
        logger.warning(f"用户不存在 - Supabase ID: {supabase_user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在，请先完成用户同步",
        )

    if not user.is_active:
        logger.warning(f"用户账号已被禁用 - ID: {user.id}, Email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账号已被禁用"
        )

    logger.info(f"✓ 用户认证成功 - ID: {user.id}, Email: {user.email}")
    return user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    可选的用户认证 - 使用 Supabase JWT

    如果提供了 token 则验证,否则返回 None
    用于既支持登录用户也支持匿名用户的端点
    """
    if credentials is None:
        return None

    try:
        payload = supabase_jwt_verifier.verify_token(credentials.credentials)
        supabase_user_id: str = payload.get("sub")
        if supabase_user_id is None:
            return None

        user = db.query(User).filter(User.supabase_user_id == supabase_user_id).first()
        if user and user.is_active:
            return user

    except HTTPException:
        # 如果 token 无效，返回 None 而不是抛出异常
        return None

    return None
