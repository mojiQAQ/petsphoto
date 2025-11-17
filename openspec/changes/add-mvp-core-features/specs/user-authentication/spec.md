## ADDED Requirements

### Requirement: Authentik OIDC 集成
系统 SHALL 集成 Authentik 作为身份提供商（IdP），使用 OpenID Connect (OIDC) 协议进行用户认证。

#### Scenario: 首次访问应用
- **WHEN** 未登录用户访问需要认证的页面
- **THEN** 系统重定向到登录页面

#### Scenario: OIDC 认证流程
- **WHEN** 用户点击登录按钮
- **THEN** 系统重定向到 Authentik 授权端点
- **AND** 用户在 Authentik 完成认证后
- **THEN** 系统接收 authorization code
- **AND** 交换 access token 和 id token
- **AND** 验证 token 签名和有效期
- **AND** 创建用户会话

#### Scenario: Token 验证失败
- **WHEN** 后端接收到无效或过期的 token
- **THEN** 返回 401 Unauthorized 错误
- **AND** 前端清除本地 token
- **AND** 重定向到登录页面

### Requirement: 邮箱密码登录
系统 SHALL 支持用户使用邮箱和密码进行注册和登录。

#### Scenario: 用户注册
- **WHEN** 用户提交注册表单（邮箱、密码、密码确认）
- **THEN** 系统验证邮箱格式有效
- **AND** 验证密码强度（至少 8 位，包含字母和数字）
- **AND** 验证两次密码一致
- **AND** 检查邮箱未被注册
- **AND** 在 Authentik 创建用户账号
- **AND** 发送验证邮件（可选）
- **AND** 返回注册成功消息

#### Scenario: 邮箱已存在
- **WHEN** 用户使用已注册的邮箱注册
- **THEN** 返回错误提示"该邮箱已被注册"
- **AND** 不创建新用户

#### Scenario: 用户登录成功
- **WHEN** 用户提交有效的邮箱和密码
- **THEN** Authentik 验证凭据
- **AND** 系统颁发 access token 和 refresh token
- **AND** 前端存储 token（localStorage 或 httpOnly cookie）
- **AND** 重定向到首页或原始请求页面

#### Scenario: 登录凭据错误
- **WHEN** 用户提交无效的邮箱或密码
- **THEN** 返回错误提示"邮箱或密码错误"
- **AND** 不泄露具体是邮箱还是密码错误

### Requirement: Token 管理
系统 SHALL 管理 access token 和 refresh token 的生命周期。

#### Scenario: Access Token 自动刷新
- **WHEN** access token 即将过期（剩余时间 < 5 分钟）
- **THEN** 前端自动使用 refresh token 请求新的 access token
- **AND** 更新存储的 token
- **AND** 继续用户操作

#### Scenario: Refresh Token 过期
- **WHEN** refresh token 已过期
- **THEN** 清除所有本地 token
- **AND** 重定向用户到登录页面
- **AND** 显示提示"会话已过期，请重新登录"

#### Scenario: 用户登出
- **WHEN** 用户点击登出按钮
- **THEN** 前端清除本地存储的所有 token
- **AND** 调用后端登出 API（可选，用于撤销 token）
- **AND** 重定向到首页

### Requirement: 用户信息管理
系统 SHALL 存储和管理用户的基本信息。

#### Scenario: 获取当前用户信息
- **WHEN** 已登录用户请求个人信息
- **THEN** 后端验证 access token
- **AND** 从 Authentik 或本地数据库获取用户信息
- **AND** 返回用户数据（ID、邮箱、用户名、积分余额）

#### Scenario: 更新用户资料
- **WHEN** 用户提交更新的用户名或头像
- **THEN** 系统验证数据有效性
- **AND** 更新数据库中的用户信息
- **AND** 返回更新成功消息

### Requirement: 密码重置
系统 SHALL 支持用户通过邮箱重置密码。

#### Scenario: 请求密码重置
- **WHEN** 用户在登录页面点击"忘记密码"
- **AND** 提交注册邮箱
- **THEN** 系统验证邮箱存在
- **AND** 生成重置 token（有效期 1 小时）
- **AND** 发送重置链接到用户邮箱
- **AND** 显示提示"重置邮件已发送"

#### Scenario: 完成密码重置
- **WHEN** 用户点击邮件中的重置链接
- **AND** 提交新密码
- **THEN** 系统验证 token 有效且未过期
- **AND** 验证新密码强度
- **AND** 更新用户密码
- **AND** 使旧 token 失效
- **AND** 重定向到登录页面

#### Scenario: 重置链接过期
- **WHEN** 用户使用过期的重置链接
- **THEN** 显示错误提示"重置链接已过期"
- **AND** 提供重新请求重置的选项

### Requirement: 前端认证状态管理
前端 SHALL 使用 React Context 或状态管理库管理认证状态。

#### Scenario: 全局认证状态
- **WHEN** 应用初始化
- **THEN** 检查本地存储的 token
- **AND** 如果 token 有效，设置用户为已登录状态
- **AND** 如果 token 无效或不存在，设置为未登录状态

#### Scenario: 受保护路由
- **WHEN** 用户访问需要认证的页面
- **THEN** 检查认证状态
- **AND** 如果未登录，重定向到登录页面
- **AND** 如果已登录，渲染页面内容

### Requirement: UI 组件设计
认证相关页面 SHALL 遵循简洁的欧美设计风格，使用 shadcn/ui 组件。

#### Scenario: 登录页面 UI
- **WHEN** 用户访问登录页面
- **THEN** 显示居中的白色卡片（阴影、圆角）
- **AND** 包含 Logo 或应用名称
- **AND** 邮箱输入框（shadcn/ui Input）
- **AND** 密码输入框（带显示/隐藏切换）
- **AND** "记住我"复选框（可选）
- **AND** 登录按钮（shadcn/ui Button，primary variant）
- **AND** "忘记密码？"链接
- **AND** "还没有账号？注册"链接
- **AND** 分隔线 + "或使用其他方式登录"（为 Phase 2 OAuth 预留）

#### Scenario: 注册页面 UI
- **WHEN** 用户访问注册页面
- **THEN** 显示类似登录页面的居中卡片
- **AND** 包含邮箱、密码、确认密码输入框
- **AND** 密码强度指示器（可选）
- **AND** 注册按钮
- **AND** "已有账号？登录"链接

#### Scenario: 表单验证反馈
- **WHEN** 用户提交表单时存在错误
- **THEN** 在对应输入框下方显示红色错误文字
- **AND** 输入框边框变为红色
- **AND** 登录/注册按钮保持可用（允许重新提交）

#### Scenario: 加载状态
- **WHEN** 用户点击登录/注册按钮
- **THEN** 按钮显示 loading spinner
- **AND** 按钮文字变为"登录中..." / "注册中..."
- **AND** 按钮禁用，防止重复提交

### Requirement: API 端点规范
后端 SHALL 提供 RESTful API 端点处理认证相关请求。

#### Scenario: API 端点列表
- **POST /api/auth/register** - 用户注册
- **POST /api/auth/login** - 用户登录
- **POST /api/auth/logout** - 用户登出
- **POST /api/auth/refresh** - 刷新 token
- **GET /api/auth/me** - 获取当前用户信息
- **PUT /api/auth/me** - 更新用户信息
- **POST /api/auth/password-reset** - 请求密码重置
- **POST /api/auth/password-reset/confirm** - 确认密码重置

#### Scenario: 标准响应格式
- **WHEN** API 请求成功
- **THEN** 返回 JSON 格式
  ```json
  {
    "success": true,
    "data": { ... },
    "message": "操作成功"
  }
  ```

#### Scenario: 错误响应格式
- **WHEN** API 请求失败
- **THEN** 返回 JSON 格式
  ```json
  {
    "success": false,
    "error": {
      "code": "AUTH_001",
      "message": "邮箱或密码错误",
      "details": {}
    }
  }
  ```

### Requirement: 数据库模型
系统 SHALL 在本地数据库存储用户的扩展信息。

#### Scenario: User 表结构
- **id**: UUID (主键)
- **authentik_user_id**: String (Authentik 用户 ID，唯一)
- **email**: String (邮箱，唯一，索引)
- **username**: String (用户名，可为空)
- **avatar_url**: String (头像 URL，可为空)
- **credits**: Integer (积分余额，默认 0)
- **created_at**: DateTime (创建时间)
- **updated_at**: DateTime (更新时间)
- **last_login_at**: DateTime (最后登录时间)

#### Scenario: 用户创建时初始化
- **WHEN** 新用户首次通过 Authentik 登录
- **THEN** 在本地数据库创建对应的 User 记录
- **AND** 初始积分为 0 或注册奖励积分（如 10）
- **AND** 记录创建时间和最后登录时间
