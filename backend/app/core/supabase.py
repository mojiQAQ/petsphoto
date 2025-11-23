"""
Supabase JWT 验证工具
"""
from typing import Dict, Optional
import jwt
import httpx
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from app.core.config import settings


class SupabaseJWTVerifier:
    """Supabase JWT 验证器"""

    def __init__(self):
        self.jwt_secret = settings.SUPABASE_JWT_SECRET
        self.supabase_url = settings.SUPABASE_URL
        self._jwks_cache: Optional[Dict] = None
        self._jwks_cache_expires_at: Optional[datetime] = None

    async def get_jwks(self) -> Dict:
        """
        获取 Supabase 的 JWKS (JSON Web Key Set)
        使用缓存以提高性能
        """
        # 如果缓存有效，直接返回
        if (
            self._jwks_cache is not None
            and self._jwks_cache_expires_at is not None
            and datetime.utcnow() < self._jwks_cache_expires_at
        ):
            return self._jwks_cache

        # 从 Supabase 获取 JWKS
        jwks_url = f"{self.supabase_url}/auth/v1/.well-known/jwks.json"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(jwks_url, timeout=10.0)
                response.raise_for_status()
                self._jwks_cache = response.json()
                # 缓存 1 小时
                self._jwks_cache_expires_at = datetime.utcnow() + timedelta(hours=1)
                return self._jwks_cache
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"无法连接到 Supabase: {str(e)}",
                )

    def verify_token(self, token: str) -> Dict:
        """
        验证 Supabase JWT token

        Args:
            token: JWT token 字符串

        Returns:
            解码后的 payload

        Raises:
            HTTPException: token 无效时抛出
        """
        import logging
        logger = logging.getLogger(__name__)

        if not self.jwt_secret:
            logger.error("Supabase JWT secret 未配置")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Supabase JWT secret 未配置",
            )

        try:
            logger.debug(f"验证 JWT token (前20字符): {token[:20]}...")

            # 使用 Supabase JWT secret 验证和解码 token
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"],
                audience="authenticated",  # Supabase 使用 "authenticated" 作为 audience
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_aud": True,
                },
            )

            # 验证 payload 必要字段
            if "sub" not in payload:
                logger.warning("Token 缺少用户 ID (sub 字段)")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token 缺少用户 ID",
                )

            logger.info(f"✓ JWT 验证成功 - Supabase ID: {payload.get('sub')}")
            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("JWT token 已过期")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token 已过期",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            logger.warning(f"JWT token 无效: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token 无效: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error(f"JWT token 验证失败: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token 验证失败: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )


# 创建全局验证器实例
supabase_jwt_verifier = SupabaseJWTVerifier()
