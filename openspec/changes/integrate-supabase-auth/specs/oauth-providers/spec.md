# Spec: OAuth Providers Integration

## Overview
集成 Google 和 GitHub OAuth 登录,允许用户使用社交账号快速登录。

## ADDED Requirements

### Requirement: System MUST Google OAuth Login
用户必须能够使用 Google 账号登录。

#### Scenario: Sign in with Google successfully
**Given** 用户访问登录页面
**When** 用户点击 "使用 Google 登录" 按钮
**Then** 调用 `supabase.auth.signInWithOAuth({ provider: 'google' })`
**And** 重定向到 Google OAuth 授权页面
**And** 用户授权后重定向回应用
**And** Supabase 创建或更新用户
**And** 前端获取 access token
**And** 前端同步用户数据到后端
**And** 用户被重定向到首页

#### Scenario: Handle Google OAuth cancellation
**Given** 用户点击 "使用 Google 登录"
**When** 用户在 Google 授权页面取消
**Then** 重定向回应用
**And** 显示 "登录已取消" 提示
**And** 用户停留在登录页面

#### Scenario: Extract user metadata from Google
**Given** 用户通过 Google 登录成功
**When** Supabase 返回用户信息
**Then** 用户信息包含 Google 头像 URL
**And** 用户信息包含 Google 显示名称
**And** 前端同步这些信息到后端

### Requirement: System MUST GitHub OAuth Login
用户必须能够使用 GitHub 账号登录。

#### Scenario: Sign in with GitHub successfully
**Given** 用户访问登录页面
**When** 用户点击 "使用 GitHub 登录" 按钮
**Then** 调用 `supabase.auth.signInWithOAuth({ provider: 'github' })`
**And** 重定向到 GitHub OAuth 授权页面
**And** 用户授权后重定向回应用
**And** Supabase 创建或更新用户
**And** 前端获取 access token
**And** 用户被重定向到首页

#### Scenario: Extract user metadata from GitHub
**Given** 用户通过 GitHub 登录成功
**When** Supabase 返回用户信息
**Then** 用户信息包含 GitHub 头像 URL
**And** 用户信息包含 GitHub username
**And** 前端同步这些信息到后端

### Requirement: System MUST OAuth Callback Handling
前端必须正确处理 OAuth 回调,检测 URL 中的 session 信息。

#### Scenario: Detect OAuth session in URL
**Given** 用户从 OAuth provider 重定向回应用
**When** URL 包含 `#access_token=...` 或 session hash
**Then** Supabase SDK 自动检测并解析 session
**And** 触发 `onAuthStateChange` 事件
**And** AuthContext 更新认证状态
**And** 清理 URL 中的 hash fragment

#### Scenario: Handle OAuth error in callback
**Given** OAuth 流程失败 (如用户拒绝授权)
**When** 重定向回应用且 URL 包含 error parameter
**Then** Supabase SDK 检测到错误
**And** 前端显示错误提示
**And** 用户停留在登录页面

### Requirement: System MUST OAuth UI Components
登录页面必须提供清晰的 OAuth 登录按钮。

#### Scenario: Display OAuth login buttons
**Given** 用户访问登录页面
**When** 页面加载
**Then** 显示 "使用 Google 登录" 按钮
**And** 显示 "使用 GitHub 登录" 按钮
**And** 按钮包含对应的品牌图标
**And** 按钮样式符合品牌指南

#### Scenario: Show loading state during OAuth redirect
**Given** 用户点击 OAuth 登录按钮
**When** 等待重定向
**Then** 按钮显示 loading spinner
**And** 按钮禁用
**And** 其他登录选项禁用

## Cross-References
- Related to: `frontend-auth-integration` - 前端认证集成
- Related to: `user-data-sync` - 用户数据同步
