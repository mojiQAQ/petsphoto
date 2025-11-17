# 切换到 Google Gemini API

## 📋 准备工作

### 1. 获取 Google AI API Key

1. 访问 Google AI Studio: https://makersuite.google.com/app/apikey
2. 使用 Google 账号登录
3. 点击 "Create API Key" 或 "Get API Key"
4. 复制生成的 API Key（格式：AIza...）

### 2. 更新配置文件

编辑 `backend/.env` 文件，修改以下两行：

```bash
# 将提供商从 mock 改为 google_ai
IMAGE_PROVIDER=google_ai

# 粘贴您的 API Key
GOOGLE_AI_API_KEY=AIzaSy...您的实际API-Key
```

### 3. 重启后端服务

配置文件更新后，后端会自动重新加载（如果使用 `--reload` 模式）。

如果没有自动重启，手动重启：

```bash
cd backend
# 按 Ctrl+C 停止当前服务
# 然后重新启动
uvicorn app.main:app --reload
```

### 4. 测试

访问前端页面 http://localhost:5176/generator，上传图片并选择风格，点击生成。

---

## 🔧 快速配置命令

如果您已经有了 API Key，可以直接运行以下命令：

```bash
# 替换 YOUR_API_KEY_HERE 为您的实际 API Key
cd /Users/moji/ground/petsphoto/backend

# 更新 IMAGE_PROVIDER
sed -i '' 's/IMAGE_PROVIDER=mock/IMAGE_PROVIDER=google_ai/' .env

# 更新 GOOGLE_AI_API_KEY（替换下面的 YOUR_API_KEY_HERE）
sed -i '' 's/GOOGLE_AI_API_KEY=.*/GOOGLE_AI_API_KEY=YOUR_API_KEY_HERE/' .env
```

---

## ⚠️ 注意事项

### Google AI 的特点

- **模型**: 使用 Gemini Pro Vision 或 Imagen
- **成本**: 按请求收费，具体查看 Google AI 定价
- **速度**: 相对较慢（10-30 秒）
- **质量**: 高质量输出

### 替代方案推荐

如果 Google AI 速度太慢或成本太高，推荐使用 **Stability AI**：

```bash
# 更便宜、更快、质量同样好
IMAGE_PROVIDER=stability_ai
STABILITY_AI_API_KEY=sk-...
```

获取 Stability AI Key: https://platform.stability.ai/account/keys

---

## 🐛 故障排查

### 问题 1: "API Key invalid"

- 检查 API Key 是否正确复制（没有多余空格）
- 确认 API Key 在 Google AI Studio 中是启用状态
- 检查 `.env` 文件格式是否正确

### 问题 2: "Quota exceeded"

- Google AI 有免费配额限制
- 查看您的配额：https://makersuite.google.com/app/apikey
- 考虑升级或切换到其他提供商

### 问题 3: 生成失败

- 查看后端日志查看详细错误信息
- 确认网络连接正常
- 检查图片格式和大小是否符合要求

---

## 📊 成本估算

Google AI 定价（仅供参考，以官方为准）：

- 文本生成：免费配额后约 $0.001/1K 字符
- 图像生成：具体查看 Imagen 定价

建议：
1. 先使用免费配额测试
2. 监控使用量
3. 考虑成本效益选择合适的提供商

---

## ✅ 验证配置

运行以下命令验证配置是否正确：

```bash
cd /Users/moji/ground/petsphoto/backend
cat .env | grep -E "(IMAGE_PROVIDER|GOOGLE_AI_API_KEY)"
```

应该看到：
```
IMAGE_PROVIDER=google_ai
GOOGLE_AI_API_KEY=AIzaSy...
```

---

## 📚 更多信息

- Google AI Studio: https://makersuite.google.com
- Gemini API 文档: https://ai.google.dev/docs
- 项目 API 配置指南: `API_SETUP_GUIDE.md`

