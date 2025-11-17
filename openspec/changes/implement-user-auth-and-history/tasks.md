# Tasks: implement-user-auth-and-history

## Backend Tasks

### 1. 实现 JWT 认证基础设施
- [ ] 安装依赖: `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`
- [ ] 创建 `app/core/security.py`:
  - 实现密码哈希函数 `hash_password(password: str) -> str`
  - 实现密码验证函数 `verify_password(plain: str, hashed: str) -> bool`
  - 实现 JWT token 生成函数 `create_access_token(data: dict) -> str`
  - 实现 JWT token 解码函数 `decode_access_token(token: str) -> dict`
- [ ] 在 `.env` 添加配置: `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- [ ] 更新 `app/core/config.py` 添加 JWT 配置字段
- **验证**: 单元测试通过,token 可以正确生成和验证

### 2. 实现认证服务层
- [ ] 创建 `app/services/auth_service.py`:
  - 实现 `register_user(email, password, full_name) -> User` 函数
  - 实现 `authenticate_user(email, password) -> User | None` 函数
  - 实现 `create_tokens(user_id, email) -> dict` 函数
  - 处理邮箱重复、密码验证等异常
- [ ] 创建 `app/schemas/auth.py` 定义请求/响应模型:
  - `RegisterRequest`, `LoginRequest`, `TokenResponse`
- **验证**: 服务函数单元测试通过

### 3. 实现认证 API 端点
- [ ] 创建 `app/api/v1/auth.py`:
  - `POST /api/v1/auth/register` - 用户注册
  - `POST /api/v1/auth/login` - 用户登录
  - `POST /api/v1/auth/refresh` - 刷新 token
  - `POST /api/v1/auth/logout` - 登出(清除 token)
- [ ] 创建 `app/api/deps.py` 实现 `get_current_user` dependency
- [ ] 注册路由到 `app/main.py`
- **验证**: 使用 curl 或 Postman 测试所有端点,返回正确的响应

### 4. 实现 Google OAuth 登录
- [ ] 安装依赖: `google-auth`, `google-auth-oauthlib`
- [ ] 在 `.env` 添加: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- [ ] 在 `app/services/auth_service.py` 添加:
  - `verify_google_token(id_token: str) -> dict` 函数
  - `get_or_create_google_user(google_data: dict) -> User` 函数
- [ ] 在 `app/api/v1/auth.py` 添加:
  - `POST /api/v1/auth/google` - Google OAuth 登录
- **验证**: 使用真实 Google ID token 测试登录成功

### 5. 实现用户历史记录 API
- [ ] 创建 `app/services/history_service.py`:
  - `get_user_history(user_id, limit, offset) -> list[GenerationJob]`
  - 添加数据库查询,包含分页和排序
- [ ] 创建 `app/schemas/history.py`:
  - `HistoryItem`, `HistoryResponse`
- [ ] 在 `app/api/v1/users.py` 添加:
  - `GET /api/v1/users/me` - 获取当前用户信息
  - `GET /api/v1/users/me/history` - 获取生成历史
- **验证**: 查询返回正确的用户历史,支持分页

### 6. 数据库迁移和索引优化
- [ ] 创建 Alembic 迁移脚本:
  - 添加 `(user_id, created_at)` 复合索引到 `generation_jobs` 表
  - 确保 `users.email` 有唯一索引
- [ ] 运行迁移: `alembic upgrade head`
- **验证**: 数据库索引创建成功,查询性能提升

## Frontend Tasks

### 7. 安装前端依赖和配置
- [ ] 安装依赖:
  - `@react-oauth/google` - Google OAuth
  - `jwt-decode` - 解码 JWT token
- [ ] 在 `.env.local` 添加: `VITE_GOOGLE_CLIENT_ID`
- **验证**: 依赖安装成功,环境变量可访问

### 8. 实现认证 Context 和状态管理
- [ ] 创建 `frontend/src/contexts/AuthContext.tsx`:
  - 提供 `user`, `isAuthenticated`, `isLoading` 状态
  - 提供 `login`, `register`, `logout`, `loginWithGoogle` 方法
  - 实现 token 存储到 localStorage
  - 实现 token 自动刷新逻辑
- [ ] 在 `App.tsx` 中包裹 `AuthProvider`
- **验证**: Context 状态正确更新,token 持久化

### 9. 实现登录和注册页面
- [ ] 创建 `frontend/src/pages/LoginPage.tsx`:
  - 邮箱输入框
  - 密码输入框
  - "登录"按钮
  - "使用 Google 登录"按钮
  - "没有账号?注册"链接
- [ ] 创建 `frontend/src/pages/RegisterPage.tsx`:
  - 邮箱输入框
  - 密码输入框(带强度提示)
  - 全名输入框
  - "注册"按钮
  - "已有账号?登录"链接
- [ ] 添加表单验证和错误提示
- [ ] 创建路由: `/login`, `/register`
- **验证**: 表单提交成功,错误提示正确显示

### 10. 实现 Google OAuth 组件
- [ ] 创建 `frontend/src/components/auth/GoogleOAuthButton.tsx`:
  - 使用 `@react-oauth/google` 的 `GoogleLogin` 组件
  - 处理成功回调,调用后端 `/api/v1/auth/google`
  - 处理错误情况
- [ ] 集成到登录和注册页面
- **验证**: Google 登录流程完整,用户信息正确保存

### 11. 更新导航栏显示用户信息
- [ ] 修改 `frontend/src/components/layout/Navbar.tsx`:
  - 未登录时显示"登录/注册"按钮
  - 已登录时显示用户邮箱和积分余额
  - 添加用户头像 Dropdown 菜单:
    - "个人资料"(链接到 `/profile`,暂时禁用)
    - "退出登录"
- **验证**: 导航栏根据登录状态正确显示

### 12. 实现生成历史组件
- [ ] 创建 `frontend/src/hooks/useInfiniteHistory.ts`:
  - 使用 React Query 的 `useInfiniteQuery`
  - 实现无限滚动逻辑
  - 自动缓存和重新验证
- [ ] 创建 `frontend/src/components/history/HistoryCard.tsx`:
  - 显示缩略图(200x200px 桌面,150x150px 移动)
  - 显示风格标签
  - 显示创建时间(相对时间)
  - Hover 显示操作按钮
- [ ] 创建 `frontend/src/components/history/GenerationHistory.tsx`:
  - 使用 Grid 布局展示历史卡片
  - 实现无限滚动(react-intersection-observer)
  - 显示 loading 和空状态
- **验证**: 历史记录正确加载和显示,滚动加载更多

### 13. 集成历史记录到生成器页面
- [ ] 修改 `frontend/src/pages/GeneratorPage.tsx`:
  - 在页面底部添加"生成历史"区域
  - 仅在用户登录时显示
  - 添加 `mt-16` 间距分隔生成区域和历史区域
- **验证**: 历史区域在正确位置显示

### 14. 优化生成结果展示尺寸
- [ ] 修改 `frontend/src/components/generator/GeneratedImagePreview.tsx`:
  - 桌面端: `max-w-[400px]`
  - 移动端: `max-w-full md:max-w-[300px]`
  - 图片使用 `aspect-square`
- [ ] 修改 `frontend/src/components/generator/ResultDialog.tsx`:
  - 桌面端: Dialog 内图片 `max-w-[600px]`
  - 移动端: Dialog 宽度 90vw
- **验证**: 生成结果在不同屏幕尺寸下显示合适

### 15. 实现历史记录操作功能
- [ ] 在 `HistoryCard` 添加操作按钮:
  - "查看大图": 打开 Dialog 显示完整图片
  - "下载": 下载生成结果
  - "重新生成": 填充源图片和风格到生成器
- [ ] 实现图片懒加载和 Skeleton 占位符
- [ ] 实现图片加载失败的 fallback UI
- **验证**: 所有操作正常工作

### 16. 添加路由保护
- [ ] 创建 `frontend/src/components/auth/ProtectedRoute.tsx`:
  - 检查用户是否登录
  - 未登录时重定向到 `/login`
- [ ] 应用到需要认证的路由(如 `/profile`)
- **验证**: 未登录用户被正确重定向

## Testing Tasks

### 17. 后端测试
- [ ] 编写认证服务单元测试 (`tests/services/test_auth_service.py`)
- [ ] 编写认证 API 集成测试 (`tests/api/test_auth.py`)
- [ ] 编写历史记录 API 测试 (`tests/api/test_history.py`)
- **验证**: 所有测试通过,覆盖率 > 80%

### 18. 前端测试
- [ ] 编写 AuthContext 测试
- [ ] 编写登录/注册表单测试
- [ ] 编写历史记录组件测试
- **验证**: 主要组件测试通过

## Documentation Tasks

### 19. 更新文档
- [ ] 更新 README 添加认证功能说明
- [ ] 添加 Google OAuth 配置指南
- [ ] 更新环境变量文档
- **验证**: 文档清晰完整

## Integration Tasks

### 20. 端到端集成测试
- [ ] 测试完整注册 → 登录 → 生成 → 查看历史流程
- [ ] 测试 Google OAuth 登录流程
- [ ] 测试 token 过期和刷新机制
- [ ] 测试移动端和桌面端响应式布局
- **验证**: 所有用户流程正常工作

## Deployment Tasks

### 21. 准备生产环境
- [ ] 设置生产环境的 Google OAuth 凭证
- [ ] 配置安全的 JWT_SECRET_KEY
- [ ] 配置 CORS 允许生产域名
- [ ] 设置 token 过期时间
- **验证**: 生产配置正确且安全
