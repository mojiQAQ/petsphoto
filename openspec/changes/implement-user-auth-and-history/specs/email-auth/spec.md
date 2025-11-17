# Spec: email-auth

## ADDED Requirements

### Requirement: 系统 SHALL 支持用户使用邮箱和密码注册账号

系统 SHALL 支持用户通过提供邮箱地址和密码创建新账号。

#### Scenario: 成功注册新用户

**Given** 用户访问注册页面
**And** 用户输入有效的邮箱地址 "user@example.com"
**And** 用户输入符合要求的密码(最少8字符,包含字母和数字)
**When** 用户点击"注册"按钮
**Then** 系统创建新用户账号
**And** 系统返回 access token 和 refresh token
**And** 用户自动登录并跳转到生成器页面

#### Scenario: 邮箱已被注册

**Given** 数据库中已存在邮箱为 "existing@example.com" 的用户
**When** 新用户尝试使用 "existing@example.com" 注册
**Then** 系统返回错误 "该邮箱已被注册"
**And** 注册表单保持在页面上

#### Scenario: 密码不符合要求

**Given** 用户访问注册页面
**When** 用户输入密码 "123" (少于8字符)
**Then** 系统显示错误提示 "密码至少需要8个字符"
**And** 注册按钮保持禁用状态

---

### Requirement: 系统 SHALL 支持用户使用邮箱和密码登录

系统 SHALL 支持已注册用户使用邮箱和密码登录系统。

#### Scenario: 成功登录

**Given** 数据库中存在用户 email="user@example.com", password="ValidPass123"
**When** 用户在登录页面输入正确的邮箱和密码
**And** 用户点击"登录"按钮
**Then** 系统验证凭证
**And** 系统返回 access token 和 refresh token
**And** 用户跳转到生成器页面
**And** 导航栏显示用户邮箱和积分余额

#### Scenario: 密码错误

**Given** 数据库中存在用户 email="user@example.com"
**When** 用户输入邮箱 "user@example.com" 和错误密码 "WrongPass"
**And** 用户点击"登录"按钮
**Then** 系统返回错误 "邮箱或密码错误"
**And** 用户保持在登录页面

#### Scenario: 用户不存在

**Given** 数据库中不存在邮箱为 "nonexistent@example.com" 的用户
**When** 用户输入邮箱 "nonexistent@example.com" 和任意密码
**Then** 系统返回错误 "邮箱或密码错误"

---

### Requirement: 系统 SHALL 使用 JWT token 进行认证

系统 SHALL 使用 JWT (JSON Web Token) 进行用户身份验证和授权。

#### Scenario: 成功验证 access token

**Given** 用户已登录并获得有效的 access token
**When** 用户访问需要认证的 API 端点 `/api/v1/users/me`
**And** 请求 Header 包含 `Authorization: Bearer <valid_token>`
**Then** 系统验证 token 的签名和过期时间
**And** 系统返回当前用户信息

#### Scenario: Token 已过期

**Given** 用户的 access token 已过期(超过15分钟)
**When** 用户访问需要认证的 API 端点
**Then** 系统返回 401 Unauthorized
**And** 返回错误消息 "Token 已过期"
**And** 前端使用 refresh token 自动刷新

#### Scenario: 使用 refresh token 获取新 access token

**Given** 用户的 access token 已过期
**And** 用户持有有效的 refresh token
**When** 前端调用 `/api/v1/auth/refresh` 并提供 refresh token
**Then** 系统验证 refresh token
**And** 系统返回新的 access token
**And** 前端使用新 token 重试之前的请求

---

### Requirement: 系统 MUST 使用安全哈希存储密码

系统 MUST 使用安全的哈希算法存储用户密码,不得明文保存。

#### Scenario: 注册时密码哈希

**Given** 用户注册时输入密码 "MySecurePass123"
**When** 系统创建用户记录
**Then** 系统使用 bcrypt 算法哈希密码
**And** 数据库中存储的是哈希值,而非明文密码
**And** 哈希值的格式类似 "$2b$12$..."

#### Scenario: 登录时密码验证

**Given** 数据库中存储用户的密码哈希值
**When** 用户登录时输入密码
**Then** 系统使用 bcrypt verify 函数验证密码
**And** 系统不会解密存储的哈希值
**And** 验证通过时允许登录
