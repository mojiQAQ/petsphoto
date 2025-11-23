"""
图像生成 API 客户端 - 支持多种 AI 服务
"""
import httpx
import asyncio
import random
import logging
import base64
import json
from typing import Dict, Optional, Literal
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)

# Google Auth imports (可选依赖)
try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    logger.warning("google-auth 未安装，Google Vertex AI 认证功能不可用")

ImageProvider = Literal["mock", "google_ai", "stability_ai", "replicate", "openrouter"]


class ImageGenerationClient(ABC):
    """图像生成客户端基类"""

    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        source_image_path: str,
        **kwargs
    ) -> Dict:
        """
        生成图像

        Args:
            prompt: 文本提示词
            source_image_path: 源图片本地路径
            **kwargs: 其他参数

        Returns:
            {
                "image_url": str,  # 生成图片的 URL 或 base64
                "provider": str,   # 使用的服务提供商
                "metadata": dict   # 额外的元数据
            }

        Raises:
            Exception: API 调用失败
        """
        pass


class MockImageClient(ImageGenerationClient):
    """
    Mock 图像生成客户端，用于本地测试
    返回随机测试图片
    """

    def __init__(self, delay_range: tuple = (5, 10)):
        self.delay_range = delay_range

    async def generate_image(
        self,
        prompt: str,
        source_image_path: str,
        **kwargs
    ) -> Dict:
        # 模拟处理延迟
        delay = random.uniform(*self.delay_range)
        logger.info(f"MockImageClient: Simulating {delay:.1f}s processing time...")
        await asyncio.sleep(delay)

        # 返回随机测试图片
        seed = random.randint(1000, 9999)
        return {
            "image_url": f"https://picsum.photos/seed/{seed}/512/512",
            "provider": "mock",
            "metadata": {
                "seed": seed,
                "prompt": prompt,
                "delay": delay,
            }
        }


class GoogleAIClient(ImageGenerationClient):
    """
    Google AI Imagen 4.0 客户端

    使用 Google Vertex AI API
    文档: https://cloud.google.com/vertex-ai/docs/generative-ai/image/generate-images
    模型: publishers/google/models/imagen-4.0-generate-001

    认证方式:
    1. Service Account JSON 文件路径 (推荐)
    2. API Key (仅用于 Google AI Studio，不适用于 Vertex AI)
    """

    def __init__(
        self,
        api_key: str,
        project_id: str,
        location: str = "us-central1",
        base_url_template: str = "https://{location}-aiplatform.googleapis.com/v1",
        model: str = "publishers/google/models/imagen-4.0-generate-001",
        service_account_path: Optional[str] = None,
        timeout: int = 90
    ):
        self.api_key = api_key
        self.project_id = project_id
        self.location = location
        self.model = model
        self.timeout = timeout
        self.service_account_path = service_account_path
        self.credentials = None

        # Vertex AI endpoint - 根据 location 动态生成
        self.base_url = base_url_template.format(location=location)

        # 加载凭证
        if GOOGLE_AUTH_AVAILABLE:
            if service_account_path:
                # 方式1: 使用 Service Account JSON 文件
                try:
                    from google.oauth2 import service_account
                    self.credentials = service_account.Credentials.from_service_account_file(
                        service_account_path,
                        scopes=['https://www.googleapis.com/auth/cloud-platform']
                    )
                    logger.info(f"✓ 已加载 Service Account 凭证: {service_account_path}")
                except Exception as e:
                    logger.error(f"✗ 加载 Service Account 失败: {e}")
                    raise
            else:
                # 方式2: 使用 Application Default Credentials (ADC)
                # 通过 gcloud auth application-default login 设置
                try:
                    import google.auth
                    self.credentials, _ = google.auth.default(
                        scopes=['https://www.googleapis.com/auth/cloud-platform']
                    )
                    logger.info("✓ 已加载 Application Default Credentials (ADC)")
                except Exception as e:
                    logger.warning(f"✗ 未找到 ADC 凭证: {e}")
                    logger.info("提示: 运行 'gcloud auth application-default login' 设置凭证")

    def _get_access_token(self) -> Optional[str]:
        """获取 OAuth2 Access Token"""
        if not self.credentials:
            return None

        try:
            from google.auth.transport.requests import Request
            # 刷新 token（如果已过期）
            if not self.credentials.valid:
                self.credentials.refresh(Request())
            return self.credentials.token
        except Exception as e:
            logger.error(f"获取 access token 失败: {e}")
            return None

    async def generate_image(
        self,
        prompt: str,
        source_image_path: str,
        **kwargs
    ) -> Dict:
        """
        使用 Google Vertex AI 模型生成图像

        支持的模型:
        - Gemini 2.5 Flash Image (使用 generateContent API)
        - Imagen 3.0/4.0 (使用 predict API)
        """
        # 构建认证头部
        headers = {"Content-Type": "application/json"}

        # 优先使用 Service Account Token，否则使用 API Key
        access_token = self._get_access_token()
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
            logger.debug("使用 Service Account Bearer Token 认证")
        else:
            # 回退到 API Key（仅适用于 Google AI Studio）
            headers["x-goog-api-key"] = self.api_key
            logger.warning("使用 API Key 认证（Vertex AI 不支持，可能失败）")

        # 读取并编码源图片
        with open(source_image_path, "rb") as f:
            image_bytes = f.read()
            image_base64 = base64.b64encode(image_bytes).decode()

        # 判断模型类型并构建相应的请求格式
        is_gemini = "gemini" in self.model.lower()

        if is_gemini:
            # Gemini 2.5 Flash Image 使用 generateContent API
            payload = {
                "contents": {
                    "role": "USER",
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        },
                        {
                            "text": prompt
                        }
                    ]
                },
                "generation_config": {
                    "response_modalities": ["IMAGE"],
                    "image_config": {
                        "aspect_ratio": "1:1"
                    }
                }
            }
            endpoint = f"{self.base_url}/projects/{self.project_id}/locations/{self.location}/{self.model}:generateContent"
        else:
            # Imagen 使用 predict API
            payload = {
                "instances": [
                    {
                        "prompt": prompt,
                        "referenceImages": [
                            {
                                "referenceType": "REFERENCE_TYPE_SUBJECT",
                                "referenceId": 1,
                                "referenceImage": {
                                    "bytesBase64Encoded": image_base64
                                },
                                "subjectImageConfig": {
                                    "subjectDescription": "a pet animal",
                                    "subjectType": "SUBJECT_TYPE_PERSON"
                                }
                            }
                        ]
                    }
                ],
                "parameters": {
                    "sampleCount": 1
                }
            }
            endpoint = f"{self.base_url}/projects/{self.project_id}/locations/{self.location}/{self.model}:predict"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                model_name = "Gemini" if is_gemini else "Imagen"
                logger.info(f"Calling Google {model_name} with prompt: {prompt[:100]}...")
                logger.debug(f"Vertex AI endpoint: {endpoint}")

                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )

                response.raise_for_status()
                result = response.json()

                logger.debug(f"Google AI response: {result}")

                # 解析响应 - Gemini 和 Imagen 的响应格式不同
                if is_gemini:
                    # Gemini 响应格式: {"candidates": [{"content": {"parts": [{"inlineData": {...}}]}}]}
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            for part in candidate["content"]["parts"]:
                                # 注意: API 返回的是 inlineData (驼峰命名), 不是 inline_data
                                if "inlineData" in part:
                                    image_data = part["inlineData"].get("data")
                                    if image_data:
                                        return {
                                            "image_url": f"data:image/png;base64,{image_data}",
                                            "provider": "google_ai",
                                            "metadata": {
                                                "model": self.model,
                                                "prompt": prompt
                                            }
                                        }
                    raise Exception("No image data in Gemini response")
                else:
                    # Imagen 响应格式: {"predictions": [{"bytesBase64Encoded": "..."}]}
                    if "predictions" in result and len(result["predictions"]) > 0:
                        prediction = result["predictions"][0]
                        image_data = None
                        if "bytesBase64Encoded" in prediction:
                            image_data = prediction["bytesBase64Encoded"]
                        elif "image" in prediction:
                            if isinstance(prediction["image"], dict) and "bytesBase64Encoded" in prediction["image"]:
                                image_data = prediction["image"]["bytesBase64Encoded"]
                            elif isinstance(prediction["image"], str):
                                image_data = prediction["image"]

                        if not image_data:
                            logger.error(f"Unexpected response structure: {prediction}")
                            raise Exception("No image data in response")

                        return {
                            "image_url": f"data:image/png;base64,{image_data}",
                            "provider": "google_ai",
                            "metadata": {
                                "model": self.model,
                                "prompt": prompt
                            }
                        }
                    raise Exception("No predictions returned from Imagen")

        except httpx.TimeoutException:
            logger.error("Google AI API timeout")
            raise Exception("图像生成超时，请稍后重试")
        except httpx.HTTPStatusError as e:
            logger.error(f"Google AI API error: {e.response.status_code}")
            raise Exception(f"Google AI API 错误: {e.response.text}")


class StabilityAIClient(ImageGenerationClient):
    """
    Stability AI (Stable Diffusion) 客户端

    支持 img2img (图生图) 功能
    文档: https://platform.stability.ai/docs/api-reference
    获取 API Key: https://platform.stability.ai/account/keys
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.stability.ai",
        model: str = "stable-diffusion-xl-1024-v1-0",
        timeout: int = 90
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    async def generate_image(
        self,
        prompt: str,
        source_image_path: str,
        **kwargs
    ) -> Dict:
        """
        使用 Stability AI 的 img2img 生成图像
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

        # 准备文件上传
        with open(source_image_path, "rb") as f:
            image_bytes = f.read()

        # 构建 multipart form data
        files = {
            "init_image": ("image.png", image_bytes, "image/png"),
        }

        data = {
            "text_prompts[0][text]": prompt,
            "text_prompts[0][weight]": 1,
            "cfg_scale": kwargs.get("cfg_scale", 7),
            "samples": 1,
            "steps": kwargs.get("steps", 30),
            "image_strength": kwargs.get("image_strength", 0.35),  # 保留原图特征
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Calling Stability AI with prompt: {prompt[:100]}...")

                endpoint = f"{self.base_url}/v1/generation/{self.model}/image-to-image"
                logger.debug(f"Stability AI endpoint: {endpoint}")

                response = await client.post(
                    endpoint,
                    headers=headers,
                    files=files,
                    data=data
                )

                response.raise_for_status()
                result = response.json()

                # 解析响应
                if "artifacts" in result and len(result["artifacts"]) > 0:
                    artifact = result["artifacts"][0]
                    image_base64 = artifact.get("base64")

                    return {
                        "image_url": f"data:image/png;base64,{image_base64}",
                        "provider": "stability_ai",
                        "metadata": {
                            "model": "sdxl-1.0",
                            "seed": artifact.get("seed"),
                            "finish_reason": artifact.get("finishReason")
                        }
                    }
                else:
                    raise Exception("No artifacts returned from Stability AI")

        except httpx.TimeoutException:
            logger.error("Stability AI timeout")
            raise Exception("图像生成超时，请稍后重试")
        except httpx.HTTPStatusError as e:
            logger.error(f"Stability AI error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 402:
                raise Exception("Stability AI: 积分不足，请充值")
            elif e.response.status_code == 429:
                raise Exception("Stability AI: 请求过于频繁，请稍后重试")
            else:
                raise Exception(f"Stability AI 错误: {e.response.text}")


class ReplicateClient(ImageGenerationClient):
    """
    Replicate 客户端

    支持多种开源图像生成模型
    文档: https://replicate.com/docs
    获取 API Key: https://replicate.com/account/api-tokens
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.replicate.com/v1",
        model: str = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        timeout: int = 120
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    async def generate_image(
        self,
        prompt: str,
        source_image_path: str,
        **kwargs
    ) -> Dict:
        """
        使用 Replicate 平台的 img2img 模型
        默认使用 SDXL img2img
        """
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

        # 读取并编码图片
        with open(source_image_path, "rb") as f:
            image_bytes = f.read()
            image_base64 = base64.b64encode(image_bytes).decode()
            image_data_uri = f"data:image/png;base64,{image_base64}"

        # 使用配置的模型
        payload = {
            "version": self.model.split(":")[-1],  # 提取版本 hash
            "input": {
                "image": image_data_uri,
                "prompt": prompt,
                "num_outputs": 1,
                "guidance_scale": kwargs.get("guidance_scale", 7.5),
                "num_inference_steps": kwargs.get("steps", 30),
                "strength": kwargs.get("strength", 0.4),
            }
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Calling Replicate with prompt: {prompt[:100]}...")

                # 创建预测
                response = await client.post(
                    f"{self.base_url}/predictions",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                prediction = response.json()

                prediction_id = prediction["id"]
                logger.info(f"Replicate prediction created: {prediction_id}")

                # 轮询等待结果
                max_attempts = 60  # 最多等待 60 次
                for attempt in range(max_attempts):
                    await asyncio.sleep(2)  # 每 2 秒检查一次

                    status_response = await client.get(
                        f"{self.base_url}/predictions/{prediction_id}",
                        headers=headers
                    )
                    status_response.raise_for_status()
                    status = status_response.json()

                    if status["status"] == "succeeded":
                        output = status.get("output")
                        if output and len(output) > 0:
                            return {
                                "image_url": output[0],  # Replicate 返回图片 URL
                                "provider": "replicate",
                                "metadata": {
                                    "prediction_id": prediction_id,
                                    "model": self.model
                                }
                            }
                        else:
                            raise Exception("Replicate 未返回输出")

                    elif status["status"] == "failed":
                        error = status.get("error", "Unknown error")
                        raise Exception(f"Replicate 生成失败: {error}")

                raise Exception("Replicate 生成超时")

        except httpx.TimeoutException:
            logger.error("Replicate timeout")
            raise Exception("图像生成超时，请稍后重试")
        except httpx.HTTPStatusError as e:
            logger.error(f"Replicate error: {e.response.status_code}")
            raise Exception(f"Replicate 错误: {e.response.text}")


class OpenRouterClient(ImageGenerationClient):
    """
    OpenRouter 客户端

    通过 OpenRouter API 访问 Gemini 等模型
    文档: https://openrouter.ai/docs
    获取 API Key: https://openrouter.ai/keys
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "google/gemini-2.5-flash",
        timeout: int = 90
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    async def generate_image(
        self,
        prompt: str,
        source_image_path: str,
        **kwargs
    ) -> Dict:
        """
        使用 OpenRouter API 生成图像

        通过 OpenAI 兼容的 chat completions 端点调用 Gemini 模型
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://petsphoto.app",
            "X-Title": "PetsPhoto"
        }

        # 读取并编码源图片
        with open(source_image_path, "rb") as f:
            image_bytes = f.read()
            image_base64 = base64.b64encode(image_bytes).decode()

        # 确定图片 MIME 类型
        mime_type = "image/jpeg"
        if source_image_path.lower().endswith(".png"):
            mime_type = "image/png"
        elif source_image_path.lower().endswith(".webp"):
            mime_type = "image/webp"

        # 构建 OpenAI 兼容的请求格式
        # 对于 Gemini 图像生成，需要明确请求生成图像
        generation_prompt = f"Based on this pet photo, generate a new artistic image in the following style: {prompt}. Generate the image directly."

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": generation_prompt
                        }
                    ]
                }
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Calling OpenRouter ({self.model}) with prompt: {prompt[:100]}...")

                endpoint = f"{self.base_url}/chat/completions"
                logger.debug(f"OpenRouter endpoint: {endpoint}")

                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )

                response.raise_for_status()
                result = response.json()

                logger.debug(f"OpenRouter response: {result}")

                # 解析响应
                if "choices" in result and len(result["choices"]) > 0:
                    choice = result["choices"][0]
                    message = choice.get("message", {})

                    # 检查 images 数组（OpenRouter Gemini 特有格式）
                    images = message.get("images", [])
                    if images and len(images) > 0:
                        for img in images:
                            if isinstance(img, dict) and img.get("type") == "image_url":
                                url = img.get("image_url", {}).get("url", "")
                                if url:
                                    return {
                                        "image_url": url,
                                        "provider": "openrouter",
                                        "metadata": {
                                            "model": self.model,
                                            "prompt": prompt
                                        }
                                    }

                    content = message.get("content")

                    # content 可能是字符串或数组（多模态响应）
                    if isinstance(content, list):
                        # 多模态响应：遍历查找图像
                        for part in content:
                            if isinstance(part, dict):
                                # 检查 inline_data 格式
                                if "inline_data" in part:
                                    inline_data = part["inline_data"]
                                    mime = inline_data.get("mime_type", "image/png")
                                    data = inline_data.get("data", "")
                                    return {
                                        "image_url": f"data:{mime};base64,{data}",
                                        "provider": "openrouter",
                                        "metadata": {
                                            "model": self.model,
                                            "prompt": prompt
                                        }
                                    }
                                # 检查 image_url 格式
                                if part.get("type") == "image_url":
                                    url = part.get("image_url", {}).get("url", "")
                                    if url:
                                        return {
                                            "image_url": url,
                                            "provider": "openrouter",
                                            "metadata": {
                                                "model": self.model,
                                                "prompt": prompt
                                            }
                                        }
                        # 没有找到图像，记录内容
                        logger.warning(f"OpenRouter multimodal response without image: {content}")
                        raise Exception("OpenRouter 未返回图像数据")
                    elif isinstance(content, str):
                        # 字符串响应：检查是否是 base64 图像
                        if content.startswith("data:image"):
                            return {
                                "image_url": content,
                                "provider": "openrouter",
                                "metadata": {
                                    "model": self.model,
                                    "prompt": prompt
                                }
                            }
                        else:
                            logger.warning(f"OpenRouter returned text instead of image: {content[:500]}")
                            raise Exception("OpenRouter 未返回图像数据，请检查模型是否支持图像生成")

                raise Exception("No choices returned from OpenRouter")

        except httpx.TimeoutException:
            logger.error("OpenRouter timeout")
            raise Exception("图像生成超时，请稍后重试")
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 401:
                raise Exception("OpenRouter: API Key 无效")
            elif e.response.status_code == 402:
                raise Exception("OpenRouter: 积分不足，请充值")
            elif e.response.status_code == 429:
                raise Exception("OpenRouter: 请求过于频繁，请稍后重试")
            else:
                raise Exception(f"OpenRouter 错误: {e.response.text}")


def create_image_client(
    provider: ImageProvider = "mock",
    api_key: Optional[str] = None,
    **kwargs
) -> ImageGenerationClient:
    """
    工厂函数：创建图像生成客户端

    Args:
        provider: 服务提供商
        api_key: API 密钥
        **kwargs: 其他参数

    Returns:
        图像生成客户端实例
    """
    if provider == "mock":
        logger.info("Creating MockImageClient for testing")
        return MockImageClient()

    elif provider == "google_ai":
        if not api_key:
            raise ValueError("Google AI requires API key")

        # 从 kwargs 获取配置参数
        project_id = kwargs.pop("project_id", None)
        location = kwargs.pop("location", "us-central1")
        base_url_template = kwargs.pop("base_url_template", "https://{location}-aiplatform.googleapis.com/v1")
        model = kwargs.pop("model", "publishers/google/models/imagen-4.0-generate-001")

        if not project_id:
            raise ValueError("Google AI (Vertex AI) requires project_id")

        logger.info(f"Creating GoogleAIClient for project: {project_id}, model: {model}")
        return GoogleAIClient(
            api_key=api_key,
            project_id=project_id,
            location=location,
            base_url_template=base_url_template,
            model=model,
            **kwargs
        )

    elif provider == "stability_ai":
        if not api_key:
            raise ValueError("Stability AI requires API key")

        # 从 kwargs 获取配置参数
        base_url = kwargs.pop("base_url", "https://api.stability.ai")
        model = kwargs.pop("model", "stable-diffusion-xl-1024-v1-0")

        logger.info(f"Creating StabilityAIClient with model: {model}")
        return StabilityAIClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            **kwargs
        )

    elif provider == "replicate":
        if not api_key:
            raise ValueError("Replicate requires API key")

        # 从 kwargs 获取配置参数
        base_url = kwargs.pop("base_url", "https://api.replicate.com/v1")
        model = kwargs.pop("model", "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b")

        logger.info(f"Creating ReplicateClient with model: {model}")
        return ReplicateClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            **kwargs
        )

    elif provider == "openrouter":
        if not api_key:
            raise ValueError("OpenRouter requires API key")

        # 从 kwargs 获取配置参数
        base_url = kwargs.pop("base_url", "https://openrouter.ai/api/v1")
        model = kwargs.pop("model", "google/gemini-2.5-flash")

        logger.info(f"Creating OpenRouterClient with model: {model}")
        return OpenRouterClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            **kwargs
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")
