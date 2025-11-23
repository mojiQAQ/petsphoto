# Spec: OpenRouter Client

## Overview

实现 OpenRouter 图像生成客户端，通过 OpenRouter API 访问 Gemini 2.5 Flash 模型。

## ADDED Requirements

### Requirement: System MUST OpenRouter Image Generation Client

The system MUST implement `OpenRouterClient` class to call Gemini models via OpenRouter API.

#### Scenario: 使用 OpenRouter 生成图像

- **Given** 配置了有效的 `OPENROUTER_API_KEY`
- **And** `IMAGE_PROVIDER` 设置为 `openrouter`
- **When** 调用图像生成服务
- **Then** 系统通过 OpenRouter API 发送请求
- **And** 返回生成的图像数据

#### Scenario: OpenRouter API Key 未配置

- **Given** `OPENROUTER_API_KEY` 为空
- **And** `IMAGE_PROVIDER` 设置为 `openrouter`
- **When** 尝试创建 OpenRouter 客户端
- **Then** 系统抛出 `ValueError` 提示需要 API Key

### Requirement: System MUST OpenAI-Compatible API Format

The system MUST use OpenRouter's OpenAI-compatible endpoint for image generation requests.

#### Scenario: 发送图像生成请求

- **Given** 有效的 API Key 和源图像
- **When** 调用 `generate_image` 方法
- **Then** 发送 POST 请求到 `https://openrouter.ai/api/v1/chat/completions`
- **And** 请求体包含 `model`、`messages` 和图像数据
- **And** 请求头包含 `Authorization: Bearer <API_KEY>`

### Requirement: System MUST OpenRouter Configuration Options

The system MUST add OpenRouter-related environment variables to the configuration.

#### Scenario: 配置 OpenRouter 参数

- **Given** 用户设置环境变量
- **When** 应用启动
- **Then** `settings.OPENROUTER_API_KEY` 加载 API Key
- **And** `settings.OPENROUTER_MODEL` 默认为 `google/gemini-2.5-flash`

## Technical Details

### API Endpoint
- Base URL: `https://openrouter.ai/api/v1`
- 模型 ID: `google/gemini-2.5-flash` (支持图像输入)

### Request Format
```python
{
    "model": "google/gemini-2.5-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,..."
                    }
                },
                {
                    "type": "text",
                    "text": "prompt here"
                }
            ]
        }
    ],
    "response_format": {
        "type": "image"
    }
}
```

### Response Handling
解析 OpenRouter 响应，提取生成的图像数据（base64 或 URL）。
