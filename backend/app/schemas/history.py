"""
历史记录相关的 Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StyleInfo(BaseModel):
    """风格信息"""
    id: str
    name: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None

    class Config:
        from_attributes = True


class HistoryItem(BaseModel):
    """历史记录项"""
    id: str
    style_id: str
    style_name: Optional[str] = None  # 从 GenerationStyle 关联获取
    custom_prompt: Optional[str] = None
    status: str
    result_image_url: Optional[str] = None
    credits_cost: int
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    """历史记录响应"""
    items: list[HistoryItem]
    total: int
    limit: int
    offset: int
    has_more: bool

    @staticmethod
    def from_jobs(jobs: list, total: int, limit: int, offset: int) -> "HistoryResponse":
        """从 GenerationJob 列表创建响应"""
        items = []
        for job in jobs:
            items.append(HistoryItem(
                id=job.id,
                style_id=job.style_id,
                style_name=None,  # 可以通过 join 获取,暂时留空
                custom_prompt=job.custom_prompt,
                status=job.status.value if hasattr(job.status, 'value') else job.status,
                result_image_url=job.result_image_url,
                credits_cost=job.credits_cost,
                error_message=job.error_message,
                created_at=job.created_at,
                completed_at=job.completed_at
            ))

        return HistoryResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
            has_more=(offset + len(items)) < total
        )
