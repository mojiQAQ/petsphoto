"""
生成相关的 Pydantic schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GenerationStyleResponse(BaseModel):
    """生成风格响应"""
    id: str
    name: str
    description: Optional[str] = None
    prompt_template: str
    sort_order: int

    class Config:
        from_attributes = True


class GenerationJobCreate(BaseModel):
    """创建生成任务请求"""
    source_image_id: str
    style_id: str


class GenerationJobResponse(BaseModel):
    """生成任务响应"""
    id: str
    user_id: str
    source_image_id: str
    style_id: str
    status: str  # "pending", "processing", "completed", "failed"
    result_image_url: Optional[str] = None
    error_message: Optional[str] = None
    credits_cost: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
