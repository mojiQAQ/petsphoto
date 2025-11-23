# Tasks: Gemini OpenRouter Migration

## Implementation Tasks

- [x] **1. 添加 OpenRouter 配置项** - 在 `config.py` 中添加 `OPENROUTER_API_KEY` 和 `OPENROUTER_MODEL` 配置
- [x] **2. 实现 OpenRouterClient** - 在 `image_generation_client.py` 中创建新的客户端类
- [x] **3. 更新工厂函数** - 在 `create_image_client` 中添加 `openrouter` provider 支持
- [x] **4. 更新 ImageProvider 类型** - 在类型定义中添加 `openrouter` 选项
- [x] **5. 更新环境变量文档** - 在 `.env.example` 中添加 OpenRouter 相关配置

## Validation Tasks

- [x] **6. 测试图像生成** - 使用 OpenRouter API 测试完整的图像生成流程
