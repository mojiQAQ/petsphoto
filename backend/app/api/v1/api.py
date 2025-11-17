"""
API v1 路由聚合
"""
from fastapi import APIRouter

from app.api.v1.endpoints import images, styles, generations, auth, users

api_router = APIRouter()

# 注册端点路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(styles.router, prefix="/styles", tags=["styles"])
api_router.include_router(generations.router, prefix="/generations", tags=["generations"])
