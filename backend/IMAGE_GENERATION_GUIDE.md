# 图像生成 API 配置指南

## 问题说明

Google AI Studio API 不支持 Imagen 图像生成模型。错误信息：
```
models/imagen is not found for API version v1beta
```

**原因**: Google AI Studio 主要提供 Gemini 文本模型，Imagen 图像生成需要通过 Google Cloud Vertex AI 访问，需要 GCP 项目和复杂配置。

## 推荐解决方案

我们推荐使用以下图像生成服务（按推荐顺序）：

---

## 方案 1: Replicate（推荐）⭐

### 优点
- ✅ 简单易用，API 稳定
- ✅ 支持多种开源模型（SDXL, Stable Diffusion 等）
- ✅ 按使用量付费，价格透明
- ✅ img2img 功能完整支持
- ✅ 代码已实现，开箱即用

### 配置步骤

#### 1. 获取 API Key
1. 访问 https://replicate.com/
2. 注册账号（可用 GitHub 登录）
3. 进入 https://replicate.com/account/api-tokens
4. 创建新的 API token
5. 复制 token（格式：`r8_xxxxxxxxxxxxx`）

#### 2. 更新 .env 文件
```bash
# 修改提供商为 replicate
IMAGE_PROVIDER=replicate

# 添加 Replicate API Key
REPLICATE_API_KEY=r8_xxxxxxxxxxxxx  # 替换为你的实际 API key
```

#### 3. 重启后端服务
```bash
# 服务会自动重载，或手动重启
# Ctrl+C 停止，然后重新运行
uvicorn app.main:app --reload
```

#### 4. 价格参考
- SDXL img2img: ~$0.004 / 次
- 免费额度: $0.01 (约 2-3 次生成)
- 充值: 按需充值，最低 $5

---

## 方案 2: Stability AI

### 优点
- ✅ 官方 Stable Diffusion API
- ✅ 高质量输出
- ✅ 代码已实现

### 缺点
- ⚠️ 价格较高
- ⚠️ 需要信用卡

### 配置步骤

#### 1. 获取 API Key
1. 访问 https://platform.stability.ai/
2. 注册账号
3. 进入 https://platform.stability.ai/account/keys
4. 创建 API key

#### 2. 更新 .env 文件
```bash
IMAGE_PROVIDER=stability_ai
STABILITY_AI_API_KEY=sk-xxxxxxxxxxxxx
```

#### 3. 价格参考
- SDXL img2img: ~$0.035 / 次
- 免费额度: $0（需要付费）

---

## 方案 3: Mock 模式（测试用）

### 适用场景
- 开发测试
- 演示功能流程
- 不需要真实 AI 生成

### 配置
```bash
IMAGE_PROVIDER=mock
```

### 说明
- 返回随机测试图片（来自 picsum.photos）
- 模拟 5-10 秒处理延迟
- 不消耗 API 额度

---

## 完整的 .env 配置示例

### 使用 Replicate（推荐）
```bash
# Image Generation API Configuration
IMAGE_PROVIDER=replicate

# Replicate API Key (从 https://replicate.com/account/api-tokens 获取)
REPLICATE_API_KEY=r8_xxxxxxxxxxxxx

# 其他服务的 key 可以留空
GOOGLE_AI_API_KEY=
STABILITY_AI_API_KEY=
```

### 使用 Mock 模式（测试）
```bash
# Image Generation API Configuration
IMAGE_PROVIDER=mock

# API keys 可以留空
GOOGLE_AI_API_KEY=
STABILITY_AI_API_KEY=
REPLICATE_API_KEY=
```

---

## 验证配置

### 1. 查看启动日志
重启后端服务后，查看日志确认配置：
```
2025-11-17 01:04:04 | INFO | app | setup_logging:80 | 图像提供商: replicate
```

### 2. 测试生成任务
1. 上传一张宠物图片
2. 选择风格并生成
3. 查看日志输出

### 3. 检查日志
```bash
tail -f backend/logs/app.log
```

成功时会看到：
```
Using replicate provider for image generation
Calling Replicate with prompt: ...
Replicate prediction created: xxx
```

---

## 常见问题

### Q1: Replicate 生成很慢怎么办？
A: Replicate 使用云端 GPU，首次启动需要 30-60 秒。后续请求会快很多。

### Q2: API 配额用完了怎么办？
A:
- Replicate: 访问 https://replicate.com/account/billing 充值
- Stability AI: 访问 https://platform.stability.ai/account/billing 充值

### Q3: 如何切换回 Google AI？
A: Google AI Studio 不支持图像生成。如需使用 Google Imagen，需要：
1. 创建 Google Cloud 项目
2. 启用 Vertex AI API
3. 配置服务账号
4. 修改代码使用 Vertex AI endpoint

这个过程较复杂，建议使用 Replicate 或 Stability AI。

### Q4: Mock 模式返回的图片是什么？
A: 随机风景图片，用于测试界面流程，不是真实的 AI 生成结果。

---

## 下一步操作

1. **立即可用**: 使用 Mock 模式测试功能
2. **推荐配置**: 注册 Replicate，获取免费额度测试
3. **生产环境**: 根据使用量选择 Replicate 或 Stability AI

---

## 技术细节

### 代码位置
- 图像生成客户端: `app/services/image_generation_client.py`
- 配置管理: `app/core/config.py`
- 生成服务: `app/services/generation_service.py`

### 支持的模型
- **Replicate**: SDXL, Stable Diffusion 1.5/2.1
- **Stability AI**: SDXL 1.0
- **Mock**: 测试图片

### 自定义模型
如需使用其他 Replicate 模型，修改 `image_generation_client.py`:
```python
model_version = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
```
