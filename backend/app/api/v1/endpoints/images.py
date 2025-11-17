"""
图片上传 API 端点
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from PIL import Image
import uuid
import os
import logging
import shutil
from typing import Set

from app.core.database import get_db
from app.core.config import settings
from app.models.image import UploadedImage
from app.schemas.image import UploadedImageResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# 允许的 MIME 类型
ALLOWED_MIME_TYPES: Set[str] = {
    "image/jpeg",
    "image/png",
    "image/webp"
}

# 允许的文件扩展名
ALLOWED_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png", ".webp"}

# 最大文件大小 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes


def validate_image_file(file: UploadFile) -> None:
    """
    验证上传的图片文件

    Args:
        file: 上传的文件对象

    Raises:
        HTTPException: 文件验证失败时抛出
    """
    # 验证 MIME 类型
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的文件类型，仅支持 JPG、PNG 和 WEBP"
        )

    # 验证文件扩展名
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的文件扩展名，仅支持 .jpg、.png 和 .webp"
        )


@router.post("/upload", response_model=UploadedImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UploadedImageResponse:
    """
    上传宠物图片

    - 接受 JPG、PNG、WEBP 格式
    - 最大文件大小：10MB
    - 返回图片元数据和存储 URL
    """
    logger.info(f"图片上传请求 - 文件名: {file.filename}, 类型: {file.content_type}")

    # 验证文件类型
    validate_image_file(file)

    # 读取文件内容
    contents = await file.read()
    file_size = len(contents)
    logger.debug(f"文件大小: {file_size / 1024:.2f} KB")

    # 验证文件大小
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文件大小超过限制，最大支持 {MAX_FILE_SIZE // (1024 * 1024)}MB"
        )

    if file_size < 1024:  # 最小 1KB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小过小，可能已损坏"
        )

    try:
        # 使用 PIL 打开图片并验证
        from io import BytesIO
        image = Image.open(BytesIO(contents))
        width, height = image.size

        # 验证图片尺寸
        if width < 128 or height < 128:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="图片尺寸过小，建议至少 512x512 像素"
            )

        # 获取真实的 MIME 类型
        mime_type = Image.MIME.get(image.format, file.content_type)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的图片文件：{str(e)}"
        )

    # 生成唯一文件名
    file_ext = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"

    # 构建存储路径
    upload_dir = os.path.join(settings.UPLOAD_DIR, "images")
    file_path = os.path.join(upload_dir, unique_filename)
    storage_path = f"/uploads/images/{unique_filename}"

    # 保存文件
    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传失败，请稍后重试"
        )

    # 创建数据库记录
    try:
        image_id = str(uuid.uuid4())
        uploaded_image = UploadedImage(
            id=image_id,
            user_id="guest",  # MVP 阶段使用访客用户
            filename=file.filename,
            storage_path=storage_path,
            file_size=file_size,
            width=width,
            height=height,
            mime_type=mime_type,
            is_temp=True  # 新上传的图片标记为临时
        )
        db.add(uploaded_image)
        db.commit()
        db.refresh(uploaded_image)

        logger.info(f"✓ 图片上传成功 - ID: {image_id}, 尺寸: {width}x{height}, 大小: {file_size / 1024:.2f}KB")
        return uploaded_image

    except Exception as e:
        # 数据库操作失败，清理已上传的文件
        logger.error(f"数据库保存失败: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="保存图片信息失败"
        )


@router.get("/{image_id}", response_model=UploadedImageResponse)
def get_image(
    image_id: str,
    db: Session = Depends(get_db),
) -> UploadedImageResponse:
    """
    获取图片信息

    Args:
        image_id: 图片 ID

    Returns:
        图片信息
    """
    image = db.query(UploadedImage).filter(UploadedImage.id == image_id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图片不存在"
        )
    return image
