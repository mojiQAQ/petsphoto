# Spec: Frontend Authentication Integration

## Overview
集成 Supabase Auth SDK 到前端应用,实现完整的认证流程,包括邮箱登录和 OAuth 社交登录。

## ADDED Requirements

### Requirement: System MUST Supabase Client Setup
前端必须正确配置和初始化 Supabase client,以便与 Supabase Auth 服务通信。

#### Scenario: Initialize Supabase client with correct configuration
**Given** 前端应用启动
**When** 导入 Supabase client
**Then** client 使用正确的项目 URL 和 anon key 初始化
**And** auth 配置启用 session 持久化
**And** auth 配置启用自动 token 刷新
**And** auth 配置检测 URL 中的 session

#### Scenario: Handle missing environment variables
**Given** Supabase URL 或 anon key 未配置
**When** 应用尝试初始化 Supabase client
**Then** 抛出清晰的错误信息
**And** 应用显示配置错误提示

### Requirement: System MUST Auth Context with Supabase
AuthContext 必须重构以使用 Supabase Auth SDK,替代自建的 JWT 认证逻辑。

#### Scenario: Monitor Supabase auth state changes
**Given** Supabase client 已初始化
**When** 用户登录或登出
**Then** AuthContext 监听 `onAuthStateChange` 事件
**And** 更新本地认证状态
**And** 同步用户数据到后端

#### Scenario: Get current Supabase session
**Given** 用户已登录
**When** 组件查询当前用户
**Then** AuthContext 返回 Supabase user 对象
**And** 返回本地应用 user 对象 (含 credits 等信息)

#### Scenario: Handle expired sessions
**Given** 用户的 session 已过期
**When** 应用尝试获取当前 session
**Then** Supabase SDK 自动尝试刷新 token
**And** 如果刷新失败,清除本地 session
**And** 重定向用户到登录页

### Requirement: System MUST Email and Password Authentication
用户必须能够使用邮箱和密码进行注册和登录。

#### Scenario: Sign up with email and password
**Given** 用户访问注册页面
**When** 用户输入有效的邮箱、密码和姓名
**And** 点击"注册"按钮
**Then** 调用 `supabase.auth.signUp()`
**And** Supabase 创建新用户
**And** 前端获取 access token
**And** 前端调用后端同步用户数据
**And** 用户被重定向到首页

#### Scenario: Sign in with email and password
**Given** 用户访问登录页面
**When** 用户输入已注册的邮箱和密码
**And** 点击"登录"按钮
**Then** 调用 `supabase.auth.signInWithPassword()`
**And** Supabase 验证凭据
**And** 前端获取 access token
**And** 前端调用后端同步用户数据
**And** 用户被重定向到之前访问的页面或首页

#### Scenario: Handle invalid credentials
**Given** 用户访问登录页面
**When** 用户输入错误的邮箱或密码
**And** 点击"登录"按钮
**Then** Supabase 返回认证错误
**And** 前端显示 "邮箱或密码错误" 提示
**And** 用户停留在登录页面

#### Scenario: Handle email already exists during signup
**Given** 用户访问注册页面
**When** 用户输入已存在的邮箱
**And** 点击"注册"按钮
**Then** Supabase 返回 "用户已存在" 错误
**And** 前端显示 "该邮箱已被注册" 提示
**And** 建议用户尝试登录或使用其他邮箱

### Requirement: System MUST Sign Out Functionality
用户必须能够安全登出,清除所有本地 session 数据。

#### Scenario: Sign out successfully
**Given** 用户已登录
**When** 用户点击"退出登录"按钮
**Then** 调用 `supabase.auth.signOut()`
**And** Supabase 清除 server-side session
**And** 前端清除 localStorage 中的 session
**And** AuthContext 重置为未认证状态
**And** 用户被重定向到登录页

#### Scenario: Handle sign out errors gracefully
**Given** 用户已登录
**When** 调用 signOut 时网络错误
**Then** 前端仍然清除本地 session
**And** 用户被重定向到登录页
**And** 显示 "已退出登录" 提示

### Requirement: System MUST Access Token Management
前端必须正确管理 Supabase JWT access token,并在 API 请求中携带。

#### Scenario: Get access token for API requests
**Given** 用户已登录
**When** 前端发起 API 请求
**Then** 从 Supabase session 获取 access_token
**And** 在 Authorization header 中携带 token
**And** 格式为 `Bearer <token>`

#### Scenario: Automatically refresh expired tokens
**Given** 用户的 access token 即将过期
**When** 前端尝试获取 token
**Then** Supabase SDK 自动使用 refresh_token 刷新
**And** 返回新的 access_token
**And** API 请求使用新 token

#### Scenario: Handle token refresh failure
**Given** 用户的 refresh_token 已过期
**When** Supabase SDK 尝试刷新 token
**Then** 刷新失败
**And** 清除本地 session
**And** 重定向用户到登录页

### Requirement: System MUST Loading and Error States
认证过程中必须提供清晰的加载和错误状态反馈。

#### Scenario: Show loading state during sign in
**Given** 用户点击"登录"按钮
**When** 等待 Supabase 响应
**Then** 登录按钮显示 loading spinner
**And** 登录按钮禁用
**And** 表单输入禁用

#### Scenario: Display authentication errors
**Given** 认证过程中发生错误
**When** Supabase 返回错误响应
**Then** 显示 Toast 通知
**And** 错误信息清晰易懂 (中文)
**And** 根据错误类型给出相应建议

#### Scenario: Show initial auth loading state
**Given** 应用启动
**When** 检查现有 Supabase session
**Then** 显示全局 loading 状态
**And** 阻止未认证的页面访问
**And** session 检查完成后隐藏 loading

## MODIFIED Requirements

### Requirement: System MUST Auth Protected Routes
受保护的路由必须使用 Supabase session 验证用户身份。

#### Scenario: Redirect unauthenticated users to login
**Given** 用户未登录
**When** 用户访问受保护的页面 (如 /generator)
**Then** 检查 Supabase session
**And** session 不存在
**And** 重定向用户到 /login
**And** 保存原始 URL 用于登录后重定向

#### Scenario: Allow authenticated users to access protected routes
**Given** 用户已登录
**When** 用户访问受保护的页面
**Then** 检查 Supabase session
**And** session 存在且有效
**And** 允许访问页面

## REMOVED Requirements

### Requirement: System MUST Custom JWT Token Management
移除自建的 JWT token 生成和存储逻辑,由 Supabase 管理。

#### Scenario: No longer store custom JWT in localStorage
**Given** 用户登录成功
**When** 存储认证信息
**Then** 不再存储自定义的 `access_token` 和 `refresh_token`
**And** 仅存储 Supabase session (由 SDK 自动管理)

### Requirement: System MUST Custom Password Validation
移除前端的自定义密码验证逻辑,由 Supabase 处理。

#### Scenario: Rely on Supabase password requirements
**Given** 用户注册新账号
**When** 输入密码
**Then** 不进行前端密码强度验证
**And** 依赖 Supabase 的密码策略
**And** 显示 Supabase 返回的密码错误信息

## Cross-References
- Related to: `oauth-providers` - OAuth 社交登录
- Related to: `backend-jwt-verification` - 后端 JWT 验证
- Related to: `user-data-sync` - 用户数据同步
