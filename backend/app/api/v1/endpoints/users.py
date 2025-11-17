"""
用户相关 API 端点
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.history import HistoryResponse
from app.services.history_service import get_user_history

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    获取当前登录用户信息
    """
    logger.info(f"获取用户信息 - ID: {current_user.id}")
    return UserResponse.from_orm(current_user)


@router.get("/me/history", response_model=HistoryResponse)
async def get_my_generation_history(
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    offset: int = Query(0, ge=0, description="偏移量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> HistoryResponse:
    """
    获取当前用户的生成历史

    - 支持分页查询
    - 按创建时间倒序排列
    - 返回总数和是否有更多数据
    """
    logger.info(f"查询用户生成历史 - 用户 ID: {current_user.id}, limit: {limit}, offset: {offset}")

    # 获取历史记录
    jobs, total = get_user_history(db, current_user.id, limit, offset)

    logger.info(f"✓ 查询成功 - 返回 {len(jobs)} 条记录,总数: {total}")

    return HistoryResponse.from_jobs(jobs, total, limit, offset)
