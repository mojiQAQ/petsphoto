"""
生成任务 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import uuid
import logging
from datetime import datetime

from app.core.database import get_db
from app.models.image import GenerationJob, GenerationStatus, UploadedImage, GenerationStyle
from app.models.user import User
from app.schemas.generation import GenerationJobCreate, GenerationJobResponse
from app.services.generation_service import process_generation_job
from app.api.deps import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=GenerationJobResponse, status_code=status.HTTP_201_CREATED)
async def create_generation_job(
    request: GenerationJobCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GenerationJobResponse:
    """
    创建 AI 图像生成任务

    - 需要登录
    - 需要提供源图片 ID 和风格 ID
    - 会扣减 1 个积分
    - 返回任务 ID 和状态
    - 触发后台任务进行处理
    """
    logger.info(f"创建生成任务请求 - 用户: {current_user.email}, 源图片: {request.source_image_id}, 风格: {request.style_id}")

    # 验证源图片存在
    source_image = db.query(UploadedImage).filter(
        UploadedImage.id == request.source_image_id
    ).first()

    if not source_image:
        logger.warning(f"源图片不存在: {request.source_image_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="源图片不存在"
        )

    # 验证风格存在
    style = db.query(GenerationStyle).filter(
        GenerationStyle.id == request.style_id
    ).first()

    if not style:
        logger.warning(f"风格不存在: {request.style_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的风格ID"
        )

    # 检查用户积分是否足够
    credits_required = 1
    if current_user.credits < credits_required:
        logger.warning(f"用户积分不足 - 用户: {current_user.email}, 当前积分: {current_user.credits}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"积分不足，需要 {credits_required} 积分，当前 {current_user.credits} 积分"
        )

    # 扣减积分
    current_user.credits -= credits_required
    logger.info(f"扣减积分 - 用户: {current_user.email}, 扣减: {credits_required}, 剩余: {current_user.credits}")

    # 创建生成任务
    job_id = str(uuid.uuid4())
    job = GenerationJob(
        id=job_id,
        user_id=current_user.id,
        source_image_id=request.source_image_id,
        style_id=request.style_id,
        status=GenerationStatus.PENDING,
        credits_cost=credits_required,
        created_at=datetime.utcnow()
    )

    db.add(job)

    # 更新源图片为非临时状态
    source_image.is_temp = False

    db.commit()
    db.refresh(job)

    logger.info(f"✓ 生成任务创建成功 - ID: {job_id}, 风格: {style.name}")

    # 触发后台任务
    background_tasks.add_task(process_generation_job, job.id, db)
    logger.info(f"后台生成任务已加入队列 - ID: {job_id}")

    return job


@router.get("/{job_id}", response_model=GenerationJobResponse)
def get_generation_job(
    job_id: str,
    db: Session = Depends(get_db),
) -> GenerationJobResponse:
    """
    获取生成任务状态

    Args:
        job_id: 任务 ID

    Returns:
        任务详情，包括状态和结果 URL（如果已完成）
    """
    logger.debug(f"查询生成任务状态 - ID: {job_id}")

    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()

    if not job:
        logger.warning(f"生成任务不存在: {job_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="生成任务不存在"
        )

    logger.debug(f"任务状态 - ID: {job_id}, Status: {job.status}")
    return job
