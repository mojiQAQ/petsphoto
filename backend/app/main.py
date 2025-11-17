"""
FastAPI 主应用
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import time
import logging

from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging_config import setup_logging
from app.api.v1.api import api_router

# 设置日志
logger = setup_logging()

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有 HTTP 请求"""
    start_time = time.time()

    # 记录请求信息
    logger.info(f"→ {request.method} {request.url.path} | Client: {request.client.host}")

    # 处理请求
    response = await call_next(request)

    # 计算处理时间
    process_time = time.time() - start_time

    # 记录响应信息
    logger.info(
        f"← {request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.3f}s"
    )

    return response


# 配置 CORS（开发环境允许所有来源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境临时允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录和子目录
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.TEMP_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "generated"), exist_ok=True)

# 挂载静态文件
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 注册 API 路由
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("初始化数据库表...")
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表初始化完成")
    logger.info(f"应用已启动，访问地址: http://localhost:8000")
    logger.info(f"API 文档: http://localhost:8000/docs")


@app.get("/")
async def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}
