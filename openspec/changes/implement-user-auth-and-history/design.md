# Design: implement-user-auth-and-history

## Architecture

### 认证架构

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │────────▶│   FastAPI    │────────▶│  Database   │
│  (React)    │◀────────│   Backend    │◀────────│  (SQLite)   │
└─────────────┘  JWT    └──────────────┘         └─────────────┘
       │                        │
       │                        │
       │ OAuth                  │ Verify
       │                        │
       ▼                        ▼
┌─────────────┐         ┌──────────────┐
│   Google    │────────▶│  JWT Service │
│   OAuth     │  ID Token│             │
└─────────────┘         └──────────────┘
```

### 组件设计

#### 后端组件
1. **认证服务** (`app/services/auth_service.py`)
   - 用户注册(邮箱+密码)
   - 用户登录(邮箱+密码)
   - Google OAuth 登录
   - JWT token 生成和验证
   - 密码哈希处理

2. **用户服务** (`app/services/user_service.py`)
   - 用户信息查询
   - 用户更新
   - 生成历史查询

3. **API 路由** (`app/api/v1/auth.py`, `app/api/v1/users.py`)
   - POST `/api/v1/auth/register` - 注册
   - POST `/api/v1/auth/login` - 登录
   - POST `/api/v1/auth/google` - Google OAuth 登录
   - POST `/api/v1/auth/refresh` - 刷新 token
   - GET `/api/v1/users/me` - 获取当前用户
   - GET `/api/v1/users/me/history` - 获取生成历史

#### 前端组件
1. **认证页面**
   - `LoginPage.tsx` - 登录页面
   - `RegisterPage.tsx` - 注册页面
   - `GoogleOAuthButton.tsx` - Google 登录按钮

2. **认证 Context** (`AuthContext.tsx`)
   - 用户状态管理
   - Token 存储和刷新
   - 登录/登出方法

3. **历史记录组件**
   - `GenerationHistory.tsx` - 历史记录容器
   - `HistoryCard.tsx` - 历史记录卡片
   - `useInfiniteHistory.ts` - 无限滚动 hook

### 数据流

#### 注册流程
```
1. 用户输入邮箱和密码
2. 前端验证输入
3. POST /api/v1/auth/register
4. 后端创建用户(密码哈希)
5. 返回 JWT tokens
6. 前端存储 tokens 并跳转到生成器页面
```

#### Google OAuth 流程
```
1. 用户点击 Google 登录按钮
2. 前端跳转到 Google OAuth 授权页面
3. 用户授权后,Google 返回 authorization code
4. 前端将 code 发送到后端
5. 后端验证 code,获取用户信息
6. 创建/更新用户,返回 JWT tokens
7. 前端存储 tokens 并跳转到生成器页面
```

#### 历史记录加载流程
```
1. 用户打开生成器页面
2. 使用 React Query 加载历史记录
3. GET /api/v1/users/me/history?limit=20&offset=0
4. 渲染历史记录卡片
5. 用户滚动到底部时,加载更多
```

## Data Models

### JWT Payload
```python
{
    "sub": "user_id",           # 用户 ID
    "email": "user@example.com",
    "exp": 1234567890,          # 过期时间
    "type": "access"            # token 类型: access/refresh
}
```

### API Response Models

#### AuthResponse
```python
{
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "user": {
        "id": "uuid",
        "email": "user@example.com",
        "full_name": "John Doe",
        "credits": 10
    }
}
```

#### GenerationHistoryResponse
```python
{
    "items": [
        {
            "id": "job_uuid",
            "source_image_url": "/uploads/...",
            "result_image_url": "/uploads/generated/...",
            "style_id": "oil_painting",
            "status": "completed",
            "created_at": "2025-01-01T00:00:00Z",
            "completed_at": "2025-01-01T00:00:30Z"
        }
    ],
    "total": 100,
    "has_more": true
}
```

## UI Design

### 生成结果尺寸
- **桌面端**: max-width: 400px, aspect-ratio: 1:1
- **移动端**: max-width: 100%, aspect-ratio: 1:1

### 历史记录卡片
- **布局**: Grid 布局, 3列(桌面) / 2列(平板) / 1列(移动)
- **卡片尺寸**: 200x200px (桌面) / 150x150px(移动)
- **信息展示**:
  - 缩略图(主体)
  - 风格标签(左上角)
  - 创建时间(底部)
  - Hover: 显示查看/下载按钮

### 响应式断点
```css
/* 移动端 */
@media (max-width: 640px) {
  grid-cols: 1
  card-size: 150px
}

/* 平板 */
@media (min-width: 641px) and (max-width: 1024px) {
  grid-cols: 2
  card-size: 180px
}

/* 桌面 */
@media (min-width: 1025px) {
  grid-cols: 3
  card-size: 200px
}
```

## Security Considerations

1. **密码安全**
   - 使用 bcrypt 哈希密码
   - 最小密码长度: 8 字符
   - 要求包含字母和数字

2. **Token 安全**
   - Access token 有效期: 15 分钟
   - Refresh token 有效期: 7 天
   - Refresh token 存储在 HttpOnly cookie 中

3. **OAuth 安全**
   - 验证 Google OAuth state 参数
   - 仅接受来自 Google 的 ID token
   - 验证 token 的 audience 和 issuer

4. **API 安全**
   - 所有需要认证的端点使用 JWT 验证
   - 历史记录只返回当前用户的数据
   - 实施请求限流

## Performance Considerations

1. **历史记录分页**
   - 默认每页 20 条
   - 使用 offset-based pagination
   - 添加数据库索引: `(user_id, created_at)`

2. **图片优化**
   - 历史记录使用缩略图
   - 懒加载图片
   - 使用 WebP 格式(后续优化)

3. **缓存策略**
   - React Query 缓存历史记录 5 分钟
   - 新生成后自动更新缓存

## Testing Strategy

### 后端测试
- 单元测试: 认证服务、密码哈希、JWT 生成
- 集成测试: API 端点测试
- Mock Google OAuth API

### 前端测试
- 组件测试: 登录/注册表单
- Hook 测试: useAuth, useInfiniteHistory
- E2E 测试: 完整认证流程(后续)

## Migration Plan

1. 创建新的 API 端点
2. 更新前端添加认证流程
3. 保持 guest 用户向后兼容(临时)
4. 逐步迁移现有功能到需要认证
5. 后续移除 guest 用户支持

## Rollback Plan

如果遇到严重问题:
1. 回滚后端 API 变更
2. 前端回退到 guest 模式
3. 保留数据库迁移,不丢失用户数据
