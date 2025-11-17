# Spec: google-oauth

## ADDED Requirements

### Requirement: 系统 SHALL 支持用户使用 Google 账号登录

系统 SHALL 支持用户通过 Google OAuth 2.0 进行一键登录,无需手动注册。

#### Scenario: 首次 Google 登录自动创建账号

**Given** 用户从未使用 Google 账号登录过系统
**And** Google 账号邮箱为 "user@gmail.com"
**When** 用户点击"使用 Google 登录"按钮
**And** 用户在 Google 授权页面点击"允许"
**And** Google 返回用户信息(email, name, picture)
**Then** 系统自动创建新用户账号
**And** 用户邮箱设置为 "user@gmail.com"
**And** 用户全名设置为 Google 返回的 name
**And** 系统生成并返回 JWT tokens
**And** 用户跳转到生成器页面

#### Scenario: 已有账号的 Google 登录

**Given** 数据库中已存在邮箱为 "existing@gmail.com" 的用户
**When** 用户使用相同的 Google 账号登录
**Then** 系统识别为现有用户
**And** 系统更新 last_login_at 时间戳
**And** 系统返回 JWT tokens
**And** 用户跳转到生成器页面

#### Scenario: Google 授权被拒绝

**Given** 用户点击"使用 Google 登录"按钮
**When** 用户在 Google 授权页面点击"拒绝"或关闭页面
**Then** 系统不创建用户
**And** 用户返回到登录页面
**And** 显示提示信息 "需要授权才能使用 Google 登录"

---

### Requirement: 系统 MUST 验证 Google OAuth 流程安全性

系统 MUST 验证 Google OAuth 返回的 ID token 的有效性和来源。

#### Scenario: 验证 Google ID token

**Given** 前端从 Google OAuth 获得 ID token
**When** 前端将 ID token 发送到后端 `/api/v1/auth/google`
**Then** 后端使用 Google 的公钥验证 token 签名
**And** 后端验证 token 的 issuer 为 "https://accounts.google.com"
**And** 后端验证 token 的 audience 为配置的 Google Client ID
**And** 后端验证 token 未过期
**And** 验证通过后提取用户信息

#### Scenario: 无效的 ID token

**Given** 前端发送了伪造的或过期的 ID token
**When** 后端验证 token
**Then** 验证失败
**And** 系统返回 401 Unauthorized
**And** 返回错误消息 "无效的 Google 凭证"

---

### Requirement: Google 登录按钮 MUST 符合 Google 品牌指南

Google 登录按钮 MUST 符合 Google 的品牌指南,包括样式和文案。

#### Scenario: Google 登录按钮样式

**Given** 用户访问登录页面
**Then** "使用 Google 登录"按钮包含 Google logo
**And** 按钮文案为中文 "使用 Google 登录"
**And** 按钮使用白色背景,带边框
**And** 按钮在 hover 时有轻微阴影效果
**And** 按钮符合 shadcn/ui Button 组件规范
