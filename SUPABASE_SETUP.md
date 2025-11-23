# Supabase Authentication 集成设置指南

本指南将帮助您完成 PetsPhoto 项目的 Supabase Authentication 集成。

## 📋 前置要求

- Node.js >= 18
- Python >= 3.10
- Supabase 账号（免费）

## 🚀 快速开始

### 第一步：创建 Supabase 项目

1. 访问 [Supabase Dashboard](https://app.supabase.com/)
2. 点击 "New Project"
3. 填写项目信息：
   - **Project Name**: petsphoto（或您喜欢的名称）
   - **Database Password**: 生成一个强密码并保存
   - **Region**: 选择离您用户最近的区域（如 `us-west-1` 或 `ap-southeast-1`）
4. 点击 "Create new project"，等待项目创建完成（约 1-2 分钟）

### 第二步：获取 Supabase 配置信息

项目创建完成后，在 Supabase Dashboard 中：

1. 进入 **Settings** → **API**
2. 记录以下信息：
   - **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
   - **anon public** key: 以 `eyJ...` 开头的长字符串

3. 进入 **Settings** → **API** → **JWT Settings**
4. 记录：
   - **JWT Secret**: 这是用于后端验证 JWT 的密钥

### 第三步：配置 OAuth Providers

#### 配置 Google OAuth

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 **Google+ API**
4. 进入 **APIs & Services** → **Credentials**
5. 点击 **Create Credentials** → **OAuth 2.0 Client ID**
6. 选择 **Web application**
7. 添加授权的重定向 URI：
   ```
   https://[您的项目ID].supabase.co/auth/v1/callback
   ```
8. 复制 **Client ID** 和 **Client Secret**

9. 返回 Supabase Dashboard：
   - 进入 **Authentication** → **Providers**
   - 找到 **Google**，点击启用
   - 粘贴 Client ID 和 Client Secret
   - 点击 **Save**

#### 配置 GitHub OAuth

1. 访问 [GitHub Developer Settings](https://github.com/settings/developers)
2. 点击 **New OAuth App**
3. 填写信息：
   - **Application name**: PetsPhoto
   - **Homepage URL**: `http://localhost:5173`（开发环境）
   - **Authorization callback URL**:
     ```
     https://[您的项目ID].supabase.co/auth/v1/callback
     ```
4. 点击 **Register application**
5. 复制 **Client ID**
6. 点击 **Generate a new client secret** 并复制

7. 返回 Supabase Dashboard：
   - 进入 **Authentication** → **Providers**
   - 找到 **GitHub**，点击启用
   - 粘贴 Client ID 和 Client Secret
   - 点击 **Save**

### 第四步：配置 Redirect URLs

在 Supabase Dashboard 中：

1. 进入 **Authentication** → **URL Configuration**
2. 添加以下 **Redirect URLs**：
   ```
   http://localhost:5173/auth/callback
   http://localhost:5176/auth/callback
   ```
   （如果有生产环境URL，也添加进去）

3. 设置 **Site URL** 为：
   ```
   http://localhost:5173
   ```

### 第五步：配置环境变量

#### 前端环境变量

编辑 `/frontend/.env` 文件：

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000

# Supabase Configuration
VITE_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Stripe Configuration
VITE_STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key

# App Configuration
VITE_APP_NAME=PetsPhoto
VITE_THEME_MODE=light
```

#### 后端环境变量

编辑 `/backend/.env` 文件：

```bash
# ===================================
# Supabase 认证配置
# ===================================
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_JWT_SECRET=your-jwt-secret-from-supabase-settings

# ===================================
# 应用配置
# ===================================
APP_NAME=PetsPhoto
DEBUG=True

# ===================================
# 数据库配置
# ===================================
DATABASE_URL=sqlite:///./petsphoto.db

# ===================================
# 安全配置
# ===================================
SECRET_KEY=your-secret-key-at-least-32-characters-long-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ... 其他配置保持不变 ...
```

### 第六步：安装依赖并运行数据库迁移

#### 后端

```bash
cd backend

# 如果使用虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
python3 -m alembic upgrade head
```

#### 前端

```bash
cd frontend

# 安装依赖（已完成，Supabase SDK 已安装）
npm install
```

### 第七步：启动应用

#### 启动后端

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

#### 启动前端

```bash
cd frontend
npm run dev
```

## ✅ 验证集成

访问 `http://localhost:5173`，您应该能够：

1. **邮箱密码注册/登录**：
   - 点击"注册"，使用邮箱和密码创建账号
   - 使用相同邮箱和密码登录

2. **Google OAuth 登录**：
   - 点击"使用 Google 登录"按钮
   - 选择 Google 账号
   - 授权后自动跳转回应用并登录

3. **GitHub OAuth 登录**：
   - 点击"使用 GitHub 登录"按钮
   - 授权 GitHub OAuth App
   - 自动跳转回应用并登录

## 🔧 故障排查

### 前端问题

**问题**: "Missing Supabase environment variables"

**解决方案**: 确保 `.env` 文件中的 `VITE_SUPABASE_URL` 和 `VITE_SUPABASE_ANON_KEY` 已正确配置

---

**问题**: OAuth 登录后没有跳转回应用

**解决方案**: 检查 Supabase Dashboard 中的 Redirect URLs 是否包含 `http://localhost:5173/auth/callback`

---

### 后端问题

**问题**: "无法验证凭证" 或 "Token 无效"

**解决方案**:
1. 确保 `SUPABASE_JWT_SECRET` 与 Supabase Dashboard 中的 JWT Secret 一致
2. 检查 JWT Secret 是否正确粘贴（注意不要有多余的空格或换行）

---

**问题**: "用户不存在，请先完成用户同步"

**解决方案**: 这是正常流程。前端会自动调用 `/api/v1/auth/sync-user` 端点同步用户。如果仍然出现此错误，检查网络请求是否成功。

---

### OAuth 问题

**问题**: Google OAuth 返回 "redirect_uri_mismatch"

**解决方案**:
1. 确保 Google Cloud Console 中的 Authorized redirect URIs 包含：
   `https://[您的项目ID].supabase.co/auth/v1/callback`
2. 注意 `http` vs `https` 的区别

---

**问题**: GitHub OAuth 失败

**解决方案**:
1. 确保 GitHub OAuth App 的 Callback URL 正确
2. 检查 Client ID 和 Client Secret 是否正确配置在 Supabase 中

## 📝 API 端点说明

### 新增端点

#### POST `/api/v1/auth/sync-user`

同步 Supabase 用户到本地数据库。

**请求头**:
```
Authorization: Bearer <Supabase JWT Token>
```

**请求体**:
```json
{
  "supabase_user_id": "xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx",
  "email": "user@example.com",
  "username": "user123",
  "avatar_url": "https://..."
}
```

**响应**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user123",
  "avatar_url": "https://...",
  "credits": 10,
  "is_active": true,
  "is_verified": true,
  "created_at": "2025-11-18T12:00:00Z",
  "supabase_user_id": "xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
}
```

### 已有端点的变更

所有需要认证的端点现在接受 Supabase JWT Token：

- `GET /api/v1/auth/me`
- `POST /api/v1/images/generate`
- 等等...

传递 Token 的方式保持不变：
```
Authorization: Bearer <token>
```

## 🎯 下一步

- [ ] 在生产环境中部署应用
- [ ] 配置生产环境的 Redirect URLs
- [ ] 启用邮箱验证（Supabase Dashboard → Authentication → Email Templates）
- [ ] 自定义 OAuth 登录后的欢迎邮件
- [ ] （可选）迁移现有用户到 Supabase

## 📚 参考资源

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Auth Guide](https://supabase.com/docs/guides/auth)
- [Google OAuth Setup](https://supabase.com/docs/guides/auth/social-login/auth-google)
- [GitHub OAuth Setup](https://supabase.com/docs/guides/auth/social-login/auth-github)

## 🐛 报告问题

如果遇到问题，请查看：
1. 浏览器控制台错误
2. 后端日志输出
3. Supabase Dashboard → Logs

需要帮助？请提供：
- 错误信息的完整截图
- 浏览器控制台日志
- 后端日志输出
