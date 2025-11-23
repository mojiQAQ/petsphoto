# Spec: User Data Synchronization

## Overview
确保 Supabase Auth 用户数据与本地数据库正确同步,保持数据一致性。

## ADDED Requirements

### Requirement: System MUST Sync User on First Login
用户首次登录时,必须将 Supabase 用户信息同步到本地数据库。

#### Scenario: Create local user record on first Supabase login
**Given** 用户首次通过 Supabase 登录
**When** 前端调用后端 `/api/v1/auth/sync-user` 接口
**Then** 后端从 JWT 提取 supabase_user_id 和 email
**And** 查询本地数据库,用户不存在
**And** 创建新的 User 记录
**And** 设置 supabase_user_id
**And** 设置 email
**And** 设置 full_name (从 user_metadata)
**And** 设置 avatar_url (从 user_metadata)
**And** 初始化 credits 为 10
**And** 返回完整的用户信息

#### Scenario: Update existing user on subsequent login
**Given** 用户已存在于本地数据库
**When** 用户再次登录并调用 sync-user
**Then** 后端查询到现有用户
**And** 更新 user metadata (如 avatar_url)
**And** 不修改 credits 等业务数据
**And** 返回完整的用户信息

### Requirement: System MUST Handle User Metadata Updates
当用户在 Supabase 更新个人信息时,本地数据库必须同步更新。

#### Scenario: Sync updated avatar from OAuth provider
**Given** 用户通过 Google OAuth 登录
**And** Google 头像 URL 发生变化
**When** 调用 sync-user 接口
**Then** 后端更新本地 User 记录的 avatar_url
**And** 保持其他字段不变

#### Scenario: Sync updated name from user metadata
**Given** 用户在 Supabase 更新了 full_name
**When** 调用 sync-user 接口
**Then** 后端更新本地 User 记录的 full_name
**And** 返回更新后的用户信息

### Requirement: System MUST Database Model Updates
User 模型必须支持 Supabase 用户关联。

#### Scenario: User model includes supabase_user_id
**Given** 定义 User 数据库模型
**When** 创建用户表
**Then** 包含 supabase_user_id 字段 (String, unique, indexed)
**And** 包含 avatar_url 字段 (String, nullable)
**And** 移除 hashed_password 字段 (或标记为 nullable/deprecated)

### Requirement: System MUST Idempotent User Sync
用户同步操作必须是幂等的,多次调用不会产生副作用。

#### Scenario: Multiple sync calls do not duplicate users
**Given** 用户已同步到本地数据库
**When** 前端多次调用 sync-user 接口
**Then** 后端仅更新现有用户记录
**And** 不创建重复的用户
**And** 每次返回相同的用户 ID

### Requirement: System MUST Handle Sync Errors Gracefully
用户同步失败时,必须提供清晰的错误信息。

#### Scenario: Handle database errors during sync
**Given** 后端尝试创建用户
**When** 数据库连接失败
**Then** 返回 500 Internal Server Error
**And** 错误信息为 "无法同步用户数据,请稍后重试"
**And** 记录详细错误日志

#### Scenario: Handle missing email in JWT
**Given** Supabase JWT 缺少 email claim
**When** 后端尝试同步用户
**Then** 返回 400 Bad Request
**And** 错误信息为 "Invalid token: missing email"

## MODIFIED Requirements

### Requirement: System MUST User Query by Supabase User ID
用户查询必须优先使用 supabase_user_id 而非 email。

#### Scenario: Query user by supabase_user_id in protected endpoints
**Given** 用户访问需要认证的接口
**When** `get_current_user` dependency 执行
**Then** 从 JWT 提取 supabase_user_id
**And** 使用 supabase_user_id 查询数据库
**And** 返回匹配的 User 对象

## REMOVED Requirements

### Requirement: System MUST Local Password Management
移除本地密码存储和管理逻辑。

#### Scenario: No longer store hashed passwords
**Given** 创建或更新用户
**When** 保存到数据库
**Then** 不写入 hashed_password 字段
**And** 密码完全由 Supabase 管理

## Cross-References
- Related to: `frontend-auth-integration` - 前端认证集成
- Related to: `backend-jwt-verification` - 后端 JWT 验证
- Related to: `oauth-providers` - OAuth 社交登录
