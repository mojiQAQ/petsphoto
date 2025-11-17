"""
图像生成服务
"""
import logging
import httpx
import uuid
import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.image import GenerationJob, GenerationStatus, UploadedImage, GenerationStyle
from app.services.image_generation_client import create_image_client
from app.core.config import settings

logger = logging.getLogger(__name__)


async def download_image(url: str, save_path: str, timeout: int = 30) -> None:
    """
    下载图片到本地

    Args:
        url: 图片 URL
        save_path: 保存路径
        timeout: 超时时间（秒）

    Raises:
        Exception: 下载失败
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()

            with open(save_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Downloaded image to {save_path}")

    except Exception as e:
        logger.error(f"Failed to download image: {e}")
        raise Exception(f"下载生成图片失败：{str(e)}")


async def process_generation_job(job_id: str, db: Session) -> None:
    """
    处理生成任务（后台任务）

    1. 更新状态为 PROCESSING
    2. 获取源图片和风格信息
    3. 调用 Veo3 API
    4. 下载并保存生成结果
    5. 更新任务状态为 COMPLETED 或 FAILED

    Args:
        job_id: 任务 ID
        db: 数据库会话
    """
    try:
        # 查询任务
        job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        if not job:
            logger.error(f"Job {job_id} not found")
            return

        # 更新状态为处理中
        job.status = GenerationStatus.PROCESSING
        db.commit()
        logger.info(f"Job {job_id} status updated to PROCESSING")

        # 获取源图片
        source_image = db.query(UploadedImage).filter(
            UploadedImage.id == job.source_image_id
        ).first()

        if not source_image:
            raise Exception("源图片不存在")

        # 获取风格
        style = db.query(GenerationStyle).filter(
            GenerationStyle.id == job.style_id
        ).first()

        if not style:
            raise Exception("风格不存在")

        # 获取源图片的本地路径
        source_image_local_path = source_image.storage_path.replace("/uploads/", "uploads/")
        if not source_image_local_path.startswith("uploads/"):
            source_image_local_path = f"uploads/{source_image_local_path}"

        # 构建 prompt
        prompt = style.prompt_template

        # 根据配置选择 API provider 和 key
        provider = settings.IMAGE_PROVIDER
        api_key = None
        client_kwargs = {}

        if provider == "google_ai":
            api_key = settings.GOOGLE_AI_API_KEY
            client_kwargs["project_id"] = settings.GOOGLE_PROJECT_ID
            client_kwargs["location"] = settings.GOOGLE_LOCATION
            client_kwargs["base_url_template"] = settings.GOOGLE_BASE_URL_TEMPLATE
            client_kwargs["model"] = settings.GOOGLE_MODEL
            if settings.GOOGLE_SERVICE_ACCOUNT_PATH:
                client_kwargs["service_account_path"] = settings.GOOGLE_SERVICE_ACCOUNT_PATH
        elif provider == "stability_ai":
            api_key = settings.STABILITY_AI_API_KEY
            client_kwargs["base_url"] = settings.STABILITY_AI_BASE_URL
            client_kwargs["model"] = settings.STABILITY_AI_MODEL
        elif provider == "replicate":
            api_key = settings.REPLICATE_API_KEY
            client_kwargs["base_url"] = settings.REPLICATE_BASE_URL
            client_kwargs["model"] = settings.REPLICATE_MODEL

        # 创建图像生成客户端
        image_client = create_image_client(
            provider=provider,
            api_key=api_key,
            **client_kwargs
        )

        logger.info(f"Using {provider} provider for image generation")

        # 调用 API 生成图像
        result = await image_client.generate_image(
            prompt=prompt,
            source_image_path=source_image_local_path
        )

        # 从结果中获取生成的图片
        generated_image_url = result.get("image_url")
        if not generated_image_url:
            raise Exception("API 未返回图片 URL")

        # 下载或保存生成的图片
        generated_filename = f"result_{uuid.uuid4()}.jpg"
        generated_dir = os.path.join(settings.UPLOAD_DIR, "generated")
        generated_path = os.path.join(generated_dir, generated_filename)

        # 检查是否是 base64 格式
        if generated_image_url.startswith("data:image"):
            # 处理 base64 图片
            import base64
            import re

            # 提取 base64 数据
            base64_data = re.sub(r'^data:image\/\w+;base64,', '', generated_image_url)
            image_data = base64.b64decode(base64_data)

            # 保存到本地
            with open(generated_path, "wb") as f:
                f.write(image_data)

            logger.info(f"Saved base64 image to {generated_path}")
        else:
            # 从 URL 下载图片
            await download_image(generated_image_url, generated_path)

        # 更新任务状态为完成
        job.status = GenerationStatus.COMPLETED
        job.result_image_url = f"/uploads/generated/{generated_filename}"
        job.completed_at = datetime.utcnow()
        db.commit()

        logger.info(f"Job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")

        # 更新任务状态为失败
        try:
            job.status = GenerationStatus.FAILED
            job.error_message = str(e)
            db.commit()
        except Exception as commit_error:
            logger.error(f"Failed to update job status: {commit_error}")
            db.rollback()
