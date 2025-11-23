# Spec: Backend JWT Verification

## Overview
后端必须能够验证 Supabase 签发的 JWT token,并从中提取用户信息。

## ADDED Requirements

### Requirement: System MUST Supabase JWT Verification
后端必须实现 Supabase JWT 验证逻辑,使用 Supabase 公钥验证 token 签名。

#### Scenario: Verify valid Supabase JWT
**Given** 前端发送带有 Authorization header 的请求
**When** 后端解析 JWT token
**Then** 从 Supabase JWKS endpoint 获取公钥
**And** 验证 JWT 签名
**And** 验证 issuer 为 Supabase URL
**And** 验证 audience 为 "authenticated"
**And** 提取 user_id (sub claim)
**And** 提取 email

#### Scenario: Reject expired JWT
**Given** 前端发送过期的 JWT
**When** 后端尝试验证 token
**Then** JWT 验证失败
**And** 返回 401 Unauthorized
**And** 错误信息为 "Token expired"

#### Scenario: Reject invalid JWT signature
**Given** 前端发送被篡改的 JWT
**When** 后端尝试验证签名
**Then** 签名验证失败
**And** 返回 401 Unauthorized
**And** 错误信息为 "Invalid token signature"

### Requirement: System MUST JWKS Caching
为提高性能,后端必须缓存 Supabase JWKS (公钥集)。

#### Scenario: Cache JWKS for performance
**Given** 后端首次验证 JWT
**When** 从 Supabase 获取 JWKS
**Then** 缓存 JWKS 到内存
**And** 设置 TTL 为 24 小时
**And** 后续验证使用缓存的 JWKS

#### Scenario: Refresh expired JWKS cache
**Given** JWKS 缓存已过期
**When** 后端验证新的 JWT
**Then** 重新从 Supabase 获取 JWKS
**And** 更新缓存

### Requirement: System MUST Dependency Injection for Current User
所有需要认证的 endpoint 必须通过 `get_current_user` dependency 获取用户。

#### Scenario: Extract user from JWT in protected endpoint
**Given** 用户访问 `/api/v1/generations/` (需要认证)
**When** endpoint 使用 `Depends(get_current_user)`
**Then** 从 JWT 提取 supabase_user_id
**And** 查询本地数据库获取完整用户信息
**And** 返回 User 对象
**And** 如果用户不存在,自动创建

## MODIFIED Requirements

### Requirement: System MUST Remove Custom JWT Generation
后端不再生成自定义 JWT token,仅验证 Supabase JWT。

#### Scenario: No longer generate JWT on login
**Given** 用户通过前端登录成功
**When** 前端调用后端 sync-user 接口
**Then** 后端不生成 JWT
**And** 后端仅验证和同步用户数据

## REMOVED Requirements

### Requirement: System MUST Password Hashing and Verification
移除密码哈希和验证逻辑,由 Supabase 处理。

#### Scenario: No longer hash passwords on registration
**Given** 新用户注册
**When** 创建用户记录
**Then** 不存储 hashed_password 字段
**And** 密码由 Supabase 管理

## Cross-References
- Related to: `frontend-auth-integration` - 前端认证集成
- Related to: `user-data-sync` - 用户数据同步
