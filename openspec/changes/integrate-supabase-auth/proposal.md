# Proposal: Integrate Supabase Authentication

## Change ID
`integrate-supabase-auth`

## Overview
将现有的自建认证系统迁移到 Supabase Authentication，实现更强大、更安全的身份验证机制，并支持多种社交登录方式（Google、GitHub、邮箱）。

### 当前状态
- 后端使用自建的 JWT 认证系统
- 仅支持邮箱+密码登录
- 密码哈希使用 passlib + bcrypt
- JWT token 由后端生成和验证
- 前端通过 AuthContext 管理认证状态

### 目标状态
- 前端集成 Supabase Auth SDK
- 前端通过 Supabase 获取 JWT token
- 后端验证 Supabase 签发的 JWT
- 支持多种登录方式:
  - Google OAuth
  - GitHub OAuth
  - 邮箱+密码
  - (可选) Magic Link

### 为什么需要这个变更？
1. **减少维护负担**: 不需要自己维护用户认证、密码重置、邮件发送等功能
2. **更好的安全性**: Supabase 提供企业级的安全保障
3. **开箱即用的 OAuth**: 轻松集成 Google、GitHub 等第三方登录
4. **更好的用户体验**: 提供更多登录选项，降低注册门槛
5. **统一的身份管理**: 所有用户数据由 Supabase 统一管理

## Motivation
当前自建的认证系统功能有限，扩展性差。随着产品发展，我们需要：
- 支持多种社交登录方式
- 提供更安全的认证机制
- 减少后端维护工作
- 提升用户注册转化率

使用 Supabase Authentication 可以快速实现这些目标，同时保持与现有系统的兼容性。

## Scope
本变更涉及以下范围：

### 前端变更
- 集成 `@supabase/supabase-js` SDK
- 重构 AuthContext 使用 Supabase Auth
- 更新登录/注册页面支持多种登录方式
- 添加 OAuth 登录按钮
- 更新 API 请求携带 Supabase JWT

### 后端变更
- 移除自建的 JWT 生成逻辑
- 实现 Supabase JWT 验证中间件
- 保持用户数据同步（Supabase Auth -> 本地数据库）
- 更新依赖项管理器配置
- 添加 Supabase webhook 处理用户事件

### 数据库变更
- User 表添加 `supabase_user_id` 字段
- 保留现有用户数据结构（credits、历史记录等）
- 数据迁移脚本（可选：迁移现有用户到 Supabase）

### 配置变更
- 添加 Supabase 项目配置（URL、API keys）
- 配置 OAuth providers（Google、GitHub）
- 更新环境变量

## Out of Scope
以下内容不在本次变更范围内：
- 迁移现有用户到 Supabase（可作为后续可选步骤）
- 实现 Two-Factor Authentication (2FA)
- 自定义邮件模板（使用 Supabase 默认模板）
- 实现角色和权限系统（当前仅需基本认证）

## Dependencies
本变更依赖于：
- Supabase 项目已创建并配置
- Google OAuth credentials 已配置
- GitHub OAuth App 已创建
- 前端和后端环境变量已更新

## Affected Components
- Frontend:
  - `src/contexts/AuthContext.tsx`
  - `src/services/auth.ts`
  - `src/pages/LoginPage.tsx`
  - `src/pages/RegisterPage.tsx`
  - `src/lib/supabase.ts` (新增)
- Backend:
  - `app/api/v1/endpoints/auth.py`
  - `app/api/deps.py`
  - `app/services/auth_service.py`
  - `app/core/security.py`
  - `app/models/user.py`

## Risks and Mitigations

### 风险 1: 用户数据迁移复杂
**影响**: 现有用户可能无法直接迁移到 Supabase
**缓解措施**:
- 保留双认证系统一段时间
- 提供用户自助迁移流程
- 仅为新用户启用 Supabase

### 风险 2: JWT 验证失败
**影响**: 用户可能无法访问需要认证的接口
**缓解措施**:
- 完整的单元测试和集成测试
- Staging 环境充分测试
- 回滚方案（保留旧代码分支）

### 风险 3: OAuth 配置错误
**影响**: 社交登录功能无法使用
**缓解措施**:
- 详细的配置文档
- 开发环境先验证
- 逐步启用 OAuth providers

### 风险 4: 成本增加
**影响**: Supabase 可能有使用成本
**缓解措施**:
- 使用 Supabase 免费套餐（足够初期使用）
- 监控 API 使用量
- 设置使用量警报

## Success Criteria
本变更成功的标准：

1. **功能完整性**
   - 用户可以通过邮箱+密码注册和登录
   - 用户可以通过 Google 账号登录
   - 用户可以通过 GitHub 账号登录
   - 前端正确获取和存储 Supabase JWT
   - 后端正确验证 Supabase JWT

2. **数据一致性**
   - 新用户数据同时存储在 Supabase 和本地数据库
   - 用户积分、历史记录等数据正确关联
   - 用户退出登录后 session 正确清理

3. **用户体验**
   - 登录流程顺畅，无明显延迟
   - 错误提示清晰友好
   - OAuth 重定向流程正常

4. **安全性**
   - JWT token 正确验证
   - 敏感信息（API keys）不泄露
   - 通过安全审计

5. **可维护性**
   - 代码清晰，注释完整
   - 有完整的单元测试和集成测试
   - 文档齐全（开发文档、部署文档）

## Alternatives Considered

### 选项 1: 继续使用 Authentik
**优点**: 原计划方案，自托管，完全控制
**缺点**: 需要额外的服务器资源，维护复杂，配置繁琐
**为什么不选**: Supabase 更轻量，集成更简单

### 选项 2: 使用 Auth0
**优点**: 功能强大，企业级方案
**缺点**: 价格昂贵，免费套餐限制较多
**为什么不选**: 成本考虑，Supabase 性价比更高

### 选项 3: 使用 Firebase Auth
**优点**: Google 官方，稳定可靠
**缺点**: 与 GCP 深度绑定，vendor lock-in 风险
**为什么不选**: Supabase 更开放，可以自托管

### 选项 4: 保持自建系统
**优点**: 完全控制，无第三方依赖
**缺点**: 维护成本高，功能有限
**为什么不选**: 不符合快速迭代的目标

## Implementation Approach

### Phase 1: 基础设施 (2 天)
1. 创建 Supabase 项目
2. 配置 OAuth providers（Google、GitHub）
3. 前端集成 Supabase SDK
4. 后端添加 JWT 验证中间件

### Phase 2: 前端集成 (3 天)
1. 重构 AuthContext
2. 更新登录页面（添加 OAuth 按钮）
3. 更新注册页面
4. 测试认证流程

### Phase 3: 后端集成 (2 天)
1. 实现 JWT 验证逻辑
2. 添加用户同步逻辑
3. 更新数据库模型
4. 迁移脚本

### Phase 4: 测试和部署 (2 天)
1. 单元测试
2. 集成测试
3. E2E 测试
4. Staging 部署和验证
5. 生产部署

**总计**: 约 9 个工作日

## Open Questions
1. 是否需要迁移现有用户到 Supabase？
   - 如果需要，迁移策略是什么？
2. 是否保留旧的邮箱+密码登录作为备选？
3. 是否需要实现 Magic Link 登录？
4. OAuth 回调 URL 的域名是什么？
5. Supabase 项目部署在哪个区域（最佳性能考虑）？

## Related Changes
- `add-mvp-core-features`: 本变更属于 MVP 功能增强
- `implement-user-auth-and-history`: 替代原有的认证实现

## References
- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Supabase JWT Verification](https://supabase.com/docs/guides/auth/server-side-rendering)
- [Google OAuth Setup](https://supabase.com/docs/guides/auth/social-login/auth-google)
- [GitHub OAuth Setup](https://supabase.com/docs/guides/auth/social-login/auth-github)
