"""
图片相关的 Pydantic schemas
"""
from pydantic import BaseModel
from datetime import datetime


class UploadedImageResponse(BaseModel):
    """上传图片响应"""
    id: str
    filename: str
    storage_path: str
    file_size: int
    width: int
    height: int
    mime_type: str
    created_at: datetime

    class Config:
        from_attributes = True
