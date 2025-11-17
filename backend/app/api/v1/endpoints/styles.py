"""
生成风格 API 端点
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.image import GenerationStyle
from app.schemas.generation import GenerationStyleResponse

router = APIRouter()


@router.get("/", response_model=List[GenerationStyleResponse])
def get_styles(
    db: Session = Depends(get_db),
) -> List[GenerationStyleResponse]:
    """
    获取所有可用的生成风格

    Returns:
        风格列表，按 sort_order 排序
    """
    styles = db.query(GenerationStyle).order_by(GenerationStyle.sort_order).all()
    return styles
