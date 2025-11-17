# Google Vertex AI Imagen 4.0 设置指南

本指南将帮助您配置 Google Vertex AI Imagen 4.0 API 认证。

## 认证方式

Vertex AI 支持两种认证方式，**任选其一**即可：

### 方式 1: Service Account JSON 文件（推荐用于生产环境）

#### 步骤 1: 创建 Service Account

1. 访问 [Google Cloud Console - Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts?project=gen-lang-client-0514546609)
2. 点击 "CREATE SERVICE ACCOUNT"
3. 填写信息：
   - **Service account name**: `petsphoto-imagen`
   - **Service account ID**: 自动生成
   - **Description**: `Service account for PetsPhoto Imagen API`
4. 点击 "CREATE AND CONTINUE"

#### 步骤 2: 授予权限

在 "Grant this service account access to project" 步骤中，添加以下角色：

- **Vertex AI User** (`roles/aiplatform.user`)

点击 "CONTINUE"，然后 "DONE"

#### 步骤 3: 创建并下载 JSON 密钥

1. 在 Service Accounts 列表中，找到刚创建的 `petsphoto-imagen`
2. 点击右侧的三点菜单 → "Manage keys"
3. 点击 "ADD KEY" → "Create new key"
4. 选择 **JSON** 格式
5. 点击 "CREATE"，JSON 文件将自动下载

#### 步骤 4: 配置应用

1. 将下载的 JSON 文件保存到安全位置，例如：
   ```
   /Users/moji/ground/petsphoto/backend/config/service-account.json
   ```

2. 在 `.env` 文件中设置路径：
   ```bash
   GOOGLE_SERVICE_ACCOUNT_PATH=/Users/moji/ground/petsphoto/backend/config/service-account.json
   ```

3. **重要**: 将此路径添加到 `.gitignore`，避免泄露凭证：
   ```bash
   echo "config/service-account.json" >> .gitignore
   ```

4. 重启后端服务

---

### 方式 2: Application Default Credentials (ADC)（推荐用于开发环境）

#### 前提条件

需要安装 [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

#### 步骤 1: 安装 gcloud CLI

```bash
# macOS (使用 Homebrew)
brew install google-cloud-sdk

# 或从官网下载安装包
# https://cloud.google.com/sdk/docs/install
```

#### 步骤 2: 初始化并登录

```bash
# 初始化 gcloud
gcloud init

# 设置项目
gcloud config set project gen-lang-client-0514546609

# 设置 Application Default Credentials
gcloud auth application-default login
```

执行 `gcloud auth application-default login` 后，会打开浏览器进行 Google 账号认证。

#### 步骤 3: 验证凭证

```bash
# 获取 access token（用于测试）
gcloud auth application-default print-access-token
```

如果成功返回 token，说明配置正确。

#### 步骤 4: 重启后端服务

后端会自动检测 ADC 凭证并使用。

---

## 验证配置

启动后端服务后，查看日志输出：

### 成功使用 Service Account
```
✓ 已加载 Service Account 凭证: /path/to/service-account.json
```

### 成功使用 ADC
```
✓ 已加载 Application Default Credentials (ADC)
```

### 认证失败
```
✗ 未找到 ADC 凭证: ...
提示: 运行 'gcloud auth application-default login' 设置凭证
```

---

## 测试 API 调用

可以使用以下 curl 命令测试 Vertex AI API（需要先获取 access token）：

```bash
# 获取 access token
ACCESS_TOKEN=$(gcloud auth application-default print-access-token)

# 测试 Imagen 4.0 API
curl -X POST \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [
      {
        "prompt": "a cute cat"
      }
    ],
    "parameters": {
      "sampleCount": 1
    }
  }' \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/gen-lang-client-0514546609/locations/us-central1/publishers/google/models/imagen-4.0-generate-001:predict"
```

---

## 常见问题

### Q: Service Account 和 ADC 有什么区别？

- **Service Account**: 使用独立的服务账号凭证，适合生产环境和 CI/CD
- **ADC**: 使用个人 Google 账号凭证，适合本地开发

### Q: 可以同时配置两种方式吗？

可以，但应用会优先使用 Service Account。如果设置了 `GOOGLE_SERVICE_ACCOUNT_PATH`，ADC 将被忽略。

### Q: 出现 401 错误怎么办？

401 错误表示认证失败，请检查：

1. Service Account JSON 文件路径是否正确
2. Service Account 是否有 `Vertex AI User` 权限
3. ADC 是否已通过 `gcloud auth application-default login` 设置
4. Access Token 是否已过期（Token 默认 1 小时有效）

### Q: 出现 403 错误怎么办？

403 错误表示权限不足，请检查：

1. Service Account 是否有 `roles/aiplatform.user` 角色
2. 项目是否启用了 Vertex AI API
3. 账号的配额是否已用尽

### Q: 如何启用 Vertex AI API？

访问 [Vertex AI API](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com?project=gen-lang-client-0514546609) 并点击 "ENABLE"

---

## 安全建议

1. **永远不要**将 Service Account JSON 文件提交到 Git
2. 定期轮换 Service Account 密钥
3. 使用最小权限原则，只授予必要的角色
4. 在生产环境使用 Service Account，避免使用个人账号
5. 监控 API 使用情况和费用

---

## 参考文档

- [Vertex AI 认证文档](https://cloud.google.com/vertex-ai/docs/authentication)
- [Imagen 4.0 模型文档](https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate-001)
- [Service Account 最佳实践](https://cloud.google.com/iam/docs/best-practices-service-accounts)
