"""
认证相关的 Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    """用户注册请求"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="密码最少8位")
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    """用户登录请求"""
    email: EmailStr
    password: str


class GoogleOAuthRequest(BaseModel):
    """Google OAuth 登录请求"""
    id_token: str = Field(..., description="Google ID token")


class SyncUserRequest(BaseModel):
    """同步 Supabase 用户请求"""
    supabase_user_id: str
    email: EmailStr
    username: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    email: str
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    credits: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None
    supabase_user_id: Optional[str] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """刷新 token 请求"""
    refresh_token: str
