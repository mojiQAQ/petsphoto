"""
用户历史记录服务
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.image import GenerationJob, GenerationStyle
from app.models.user import User


def get_user_history(
    db: Session,
    user_id: str,
    limit: int = 20,
    offset: int = 0
) -> tuple[List[GenerationJob], int]:
    """
    获取用户的生成历史

    Args:
        db: 数据库会话
        user_id: 用户 ID
        limit: 每页记录数
        offset: 偏移量

    Returns:
        tuple: (生成任务列表, 总数)
    """
    # 查询总数
    total = db.query(GenerationJob).filter(
        GenerationJob.user_id == user_id
    ).count()

    # 查询分页数据,按创建时间倒序
    jobs = db.query(GenerationJob).filter(
        GenerationJob.user_id == user_id
    ).order_by(
        desc(GenerationJob.created_at)
    ).limit(limit).offset(offset).all()

    return jobs, total


def get_generation_job_with_style(
    db: Session,
    job_id: str,
    user_id: str
) -> Optional[tuple[GenerationJob, Optional[GenerationStyle]]]:
    """
    获取单个生成任务及其风格信息

    Args:
        db: 数据库会话
        job_id: 任务 ID
        user_id: 用户 ID (用于权限验证)

    Returns:
        Optional[tuple]: (生成任务, 风格) 或 None
    """
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id,
        GenerationJob.user_id == user_id
    ).first()

    if not job:
        return None

    # 查询风格信息
    style = db.query(GenerationStyle).filter(
        GenerationStyle.id == job.style_id
    ).first()

    return job, style
