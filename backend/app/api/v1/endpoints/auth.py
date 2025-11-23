"""
认证 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
    SyncUserRequest
)
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_tokens,
    verify_refresh_token,
    UserAlreadyExistsError,
    AuthenticationError
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    用户注册

    - 使用邮箱和密码注册新账号
    - 返回 JWT tokens 和用户信息
    """
    logger.info(f"用户注册请求 - 邮箱: {request.email}")

    try:
        # 创建用户
        user = register_user(
            db=db,
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )

        # 生成 tokens
        tokens = create_tokens(user.id, user.email)

        logger.info(f"✓ 用户注册成功 - ID: {user.id}, 邮箱: {user.email}")

        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user=UserResponse.from_orm(user)
        )

    except UserAlreadyExistsError as e:
        logger.warning(f"注册失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    用户登录

    - 使用邮箱和密码登录
    - 返回 JWT tokens 和用户信息
    """
    logger.info(f"用户登录请求 - 邮箱: {request.email}")

    # 验证用户
    user = authenticate_user(db, request.email, request.password)

    if not user:
        logger.warning(f"登录失败 - 邮箱或密码错误: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成 tokens
    tokens = create_tokens(user.id, user.email)

    logger.info(f"✓ 用户登录成功 - ID: {user.id}, 邮箱: {user.email}")

    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        user=UserResponse.from_orm(user)
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    刷新 access token

    - 使用 refresh token 获取新的 access token
    """
    logger.info("刷新 token 请求")

    # 验证 refresh token
    user = verify_refresh_token(db, request.refresh_token)

    if not user:
        logger.warning("刷新 token 失败 - token 无效或已过期")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效或过期的 refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成新的 tokens
    tokens = create_tokens(user.id, user.email)

    logger.info(f"✓ Token 刷新成功 - 用户 ID: {user.id}")

    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        user=UserResponse.from_orm(user)
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    用户登出

    - 前端应删除存储的 tokens
    - 这里只做验证用户登录状态
    """
    logger.info(f"用户登出 - ID: {current_user.id}, 邮箱: {current_user.email}")

    return {
        "message": "登出成功",
        "user_id": current_user.id
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    获取当前登录用户信息
    """
    logger.info(f"获取用户信息 - ID: {current_user.id}")

    return UserResponse.from_orm(current_user)


@router.post("/sync-user", response_model=UserResponse)
async def sync_user(
    request: SyncUserRequest,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    同步 Supabase 用户到本地数据库

    - 如果用户不存在则创建
    - 如果用户已存在则更新信息
    - 需要客户端传递 Supabase JWT 进行验证
    """
    logger.info(f"同步用户请求 - Supabase ID: {request.supabase_user_id}, 邮箱: {request.email}")

    # 先通过 supabase_user_id 查询
    user = db.query(User).filter(User.supabase_user_id == request.supabase_user_id).first()

    if user:
        # 用户已存在（通过 supabase_user_id 找到）
        logger.info(f"找到现有用户（通过 Supabase ID） - 用户 ID: {user.id}")
        user.email = request.email
        if request.username:
            user.username = request.username
        if request.avatar_url:
            user.avatar_url = request.avatar_url
        db.commit()
        db.refresh(user)
        logger.info(f"✓ 用户信息已更新 - ID: {user.id}")
    else:
        # 通过 supabase_user_id 未找到，尝试通过 email 查找
        user = db.query(User).filter(User.email == request.email).first()

        if user:
            # 用户存在但 supabase_user_id 不同或为空，更新 supabase_user_id
            logger.info(f"找到现有用户（通过 Email） - 用户 ID: {user.id}, 旧 Supabase ID: {user.supabase_user_id}, 新 Supabase ID: {request.supabase_user_id}")
            user.supabase_user_id = request.supabase_user_id
            user.email = request.email
            if request.username:
                user.username = request.username
            if request.avatar_url:
                user.avatar_url = request.avatar_url
            db.commit()
            db.refresh(user)
            logger.info(f"✓ 用户 Supabase ID 已更新 - ID: {user.id}")
        else:
            # 完全新用户，创建
            logger.info(f"创建新用户 - Supabase ID: {request.supabase_user_id}")
            user = User(
                email=request.email,
                username=request.username or request.email.split('@')[0],
                avatar_url=request.avatar_url,
                supabase_user_id=request.supabase_user_id,
                credits=10,  # 新用户赠送 10 积分
                is_active=True,
                is_verified=True  # Supabase 用户默认已验证
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"✓ 新用户创建成功 - ID: {user.id}")

    return UserResponse.from_orm(user)
