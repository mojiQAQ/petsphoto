"""
用户模型
"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class User(Base):
    """用户表"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)  # OAuth 用户可能没有密码
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    # 积分系统
    credits = Column(Integer, default=0)

    # 认证相关
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    supabase_user_id = Column(String, nullable=True, unique=True, index=True)  # Supabase 用户 ID
    authentik_user_id = Column(String, nullable=True, unique=True)  # Authentik 用户 ID (deprecated)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
