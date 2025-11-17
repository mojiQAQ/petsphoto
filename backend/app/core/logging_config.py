"""
日志配置模块
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings


def setup_logging():
    """
    配置应用日志

    - 开发模式：输出到控制台，DEBUG 级别
    - 生产模式：输出到文件 + 控制台，INFO 级别
    """
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 设置日志级别
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # 创建根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # 清除已有的处理器
    root_logger.handlers.clear()

    # 定义日志格式
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台处理器（彩色输出）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 文件处理器（所有日志）
    file_handler = RotatingFileHandler(
        filename=log_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # 错误日志文件处理器
    error_handler = RotatingFileHandler(
        filename=log_dir / "error.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)

    # 设置第三方库的日志级别（减少噪音）
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # 应用日志记录器
    app_logger = logging.getLogger("app")
    app_logger.setLevel(log_level)

    app_logger.info("=" * 80)
    app_logger.info(f"应用启动 - {settings.APP_NAME}")
    app_logger.info(f"调试模式: {settings.DEBUG}")
    app_logger.info(f"日志级别: {logging.getLevelName(log_level)}")
    app_logger.info(f"图像提供商: {settings.IMAGE_PROVIDER}")

    # 显示 Google AI 配置（如果使用）
    if settings.IMAGE_PROVIDER == "google_ai":
        app_logger.info(f"Google Project ID: {settings.GOOGLE_PROJECT_ID}")
        app_logger.info(f"Google Location: {settings.GOOGLE_LOCATION}")
        app_logger.info(f"Google Model: {settings.GOOGLE_MODEL}")

    app_logger.info("=" * 80)

    return app_logger
