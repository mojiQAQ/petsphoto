"""
Veo3 API 客户端
"""
import httpx
import asyncio
import random
import logging
from typing import Dict, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class Veo3ClientBase(ABC):
    """Veo3 客户端基类"""

    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        source_image_url: str,
        **kwargs
    ) -> Dict:
        """
        生成图像

        Args:
            prompt: 文本提示词
            source_image_url: 源图片 URL
            **kwargs: 其他参数

        Returns:
            包含生成图片 URL 的字典

        Raises:
            Exception: API 调用失败
        """
        pass


class Veo3Client(Veo3ClientBase):
    """
    Veo3 API 真实客户端

    注意：这是真实 API 的实现框架，需要根据实际 Veo3 API 文档调整
    """

    def __init__(self, api_key: str, api_url: str = "https://api.veo3.example.com/v1", timeout: int = 60):
        """
        初始化 Veo3 客户端

        Args:
            api_key: API 密钥
            api_url: API 基础 URL
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout

    async def generate_image(
        self,
        prompt: str,
        source_image_url: str,
        **kwargs
    ) -> Dict:
        """
        调用 Veo3 API 生成图像

        Args:
            prompt: 文本提示词描述期望的风格
            source_image_url: 源图片的完整 URL
            **kwargs: 额外的 API 参数

        Returns:
            API 响应字典，包含生成的图片 URL

        Raises:
            httpx.TimeoutException: 请求超时
            httpx.HTTPStatusError: HTTP 错误状态
            Exception: 其他错误
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 构建请求 payload
        # 注意：这是示例格式，需要根据实际 Veo3 API 文档调整
        payload = {
            "prompt": prompt,
            "image_url": source_image_url,
            "num_outputs": kwargs.get("num_outputs", 1),
            "guidance_scale": kwargs.get("guidance_scale", 7.5),
            "num_inference_steps": kwargs.get("num_inference_steps", 50),
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Calling Veo3 API with prompt: {prompt[:100]}...")

                response = await client.post(
                    f"{self.api_url}/generate",
                    json=payload,
                    headers=headers
                )

                response.raise_for_status()
                result = response.json()

                logger.info("Veo3 API call successful")
                return result

        except httpx.TimeoutException as e:
            logger.error(f"Veo3 API timeout: {e}")
            raise Exception("API 请求超时，请稍后重试")

        except httpx.HTTPStatusError as e:
            logger.error(f"Veo3 API HTTP error: {e.response.status_code} - {e.response.text}")

            if e.response.status_code == 429:
                raise Exception("API 限流：请求过于频繁，请稍后重试")
            elif e.response.status_code >= 500:
                raise Exception("图像生成服务暂时不可用，请稍后重试")
            else:
                raise Exception(f"生成失败：{e.response.text}")

        except Exception as e:
            logger.error(f"Veo3 API error: {e}")
            raise


class MockVeo3Client(Veo3ClientBase):
    """
    Mock Veo3 客户端，用于本地测试

    返回预设的示例图片，模拟真实 API 的延迟
    """

    def __init__(self, delay_range: tuple = (5, 10)):
        """
        初始化 Mock 客户端

        Args:
            delay_range: 模拟延迟的范围（秒），例如 (5, 10) 表示 5-10 秒
        """
        self.delay_range = delay_range

    async def generate_image(
        self,
        prompt: str,
        source_image_url: str,
        **kwargs
    ) -> Dict:
        """
        模拟生成图像

        Args:
            prompt: 文本提示词（未使用）
            source_image_url: 源图片 URL（未使用）
            **kwargs: 其他参数（未使用）

        Returns:
            包含示例图片 URL 的字典
        """
        # 模拟 API 处理时间
        delay = random.uniform(*self.delay_range)
        logger.info(f"MockVeo3Client: Simulating {delay:.1f}s processing time...")
        await asyncio.sleep(delay)

        # 返回示例结果
        # 注意：这里使用一个公开的测试图片 URL
        # 在实际部署前，应该替换为本地的测试图片
        result = {
            "image_url": "https://picsum.photos/seed/pet/512/512",  # 随机图片服务
            "seed": random.randint(1000, 9999),
            "model_version": "mock-v1",
            "prompt": prompt,
        }

        logger.info("MockVeo3Client: Image generation completed")
        return result


def create_veo3_client(
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    use_mock: bool = False,
    **kwargs
) -> Veo3ClientBase:
    """
    工厂函数：创建 Veo3 客户端

    Args:
        api_key: API 密钥
        api_url: API URL
        use_mock: 是否使用 Mock 客户端
        **kwargs: 其他参数

    Returns:
        Veo3 客户端实例
    """
    if use_mock:
        logger.info("Creating MockVeo3Client for testing")
        return MockVeo3Client()
    else:
        if not api_key:
            raise ValueError("API key is required for real Veo3Client")
        logger.info("Creating real Veo3Client")
        return Veo3Client(api_key=api_key, api_url=api_url or "https://api.veo3.example.com/v1", **kwargs)
