"""
图片相关模型
"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class UploadedImage(Base):
    """上传图片表"""

    __tablename__ = "uploaded_images"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # 字节
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    is_temp = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class GenerationStatus(str, enum.Enum):
    """生成任务状态"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerationJob(Base):
    """生成任务表"""

    __tablename__ = "generation_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    source_image_id = Column(String, ForeignKey("uploaded_images.id"), nullable=False)
    style_id = Column(String, nullable=False)
    custom_prompt = Column(String, nullable=True)
    status = Column(SQLEnum(GenerationStatus), default=GenerationStatus.PENDING)
    queue_position = Column(Integer, nullable=True)
    result_image_url = Column(String, nullable=True)
    credits_cost = Column(Integer, default=1)
    error_message = Column(String, nullable=True)
    api_response = Column(String, nullable=True)  # JSON string

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class GenerationStyle(Base):
    """预设风格表"""

    __tablename__ = "generation_styles"

    id = Column(String, primary_key=True)  # 如 "cartoon"
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    prompt_template = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
