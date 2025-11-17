# Proposal: implement-user-auth-and-history

## Summary

实现完整的用户认证系统和生成历史功能,包括邮箱注册登录、Google OAuth 登录,以及在生成器页面展示用户的所有生成历史记录。


## Why

当前系统缺乏用户认证和历史记录管理,导致以下问题:
1. 用户无法保存和查看历史生成记录
2. 无法实现个性化功能和积分系统
3. 缺乏用户留存和回访机制
4. 难以进行用户行为分析和产品优化

实现用户认证和历史记录功能后:
- 用户可以随时查看和下载历史生成的图片
- 支持积分系统和付费功能
- 提升用户留存率和产品粘性
- 为后续功能(如收藏、分享)打下基础

## What Changes

- 添加邮箱密码注册和登录功能
- 集成 Google OAuth 2.0 登录
- 实现 JWT token 认证机制
- 添加用户生成历史查询 API
- 在生成器页面底部展示历史记录
- 优化生成结果和历史记录图片尺寸

## Impact

- 影响的 specs: email-auth, google-oauth, generation-history, ui-optimization (全部为新增)
- 影响的代码:
  - Backend: `app/core/security.py` (新增), `app/services/auth_service.py` (新增), `app/api/v1/auth.py` (新增)
  - Frontend: `src/contexts/AuthContext.tsx` (新增), `src/pages/LoginPage.tsx` (新增), `src/components/history/` (新增目录)

## Motivation

当前系统使用 guest 用户进行图片生成,缺乏用户账号管理和历史记录功能。为了提供完整的用户体验,需要实现:

1. **用户认证**: 允许用户通过邮箱或 Google 账号注册和登录
2. **生成历史**: 用户可以查看所有历史生成记录
3. **持久化展示**: 在生成页面下方持续展示历史记录,方便用户快速查看和重新使用
4. **UI 优化**: 优化生成结果和历史记录的显示尺寸,避免占用过多空间

## Scope

### In Scope
- 邮箱密码注册和登录
- Google OAuth 登录集成
- JWT token 认证机制
- 用户生成历史查询 API
- 生成器页面底部历史记录展示
- 生成结果图片尺寸优化
- 历史记录卡片尺寸优化

### Out of Scope
- Authentik 集成(简化为直接 JWT 认证)
- 密码重置功能(后续迭代)
- 邮箱验证(后续迭代)
- 用户个人资料编辑(后续迭代)
- 社交分享功能(后续迭代)

## Dependencies

- 依赖现有的 User 和 GenerationJob 模型
- 需要前端路由支持(React Router)
- 需要状态管理支持(React Query)
-需要 Google OAuth 2.0 客户端凭证

## Risks

1. **安全风险**: JWT token 存储和刷新机制需要正确实现
2. **性能风险**: 历史记录查询可能随用户增长变慢,需要分页和索引优化
3. **UI/UX 风险**: 历史记录展示布局需要平衡信息密度和可读性

## Alternatives Considered

1. **Authentik vs JWT**: 考虑使用 Authentik 作为 IdP,但为了简化实现,选择直接 JWT 认证
2. **单独历史页面 vs 生成页面集成**: 选择在生成页面集成,提供更流畅的用户体验
3. **无限滚动 vs 分页**: 选择无限滚动,提供更现代的交互体验

## Success Metrics

- 用户可以成功注册和登录
- Google OAuth 登录成功率 > 95%
- 历史记录加载时间 < 2 秒
- 生成结果和历史记录卡片尺寸符合 UI 设计规范
- 移动端和桌面端布局正确响应

## Open Questions

1. 历史记录默认加载多少条?(建议: 初始 20 条,滚动加载更多)
2. 历史记录卡片的最佳尺寸是多少?(需要 UI 设计确认)
3. 是否需要历史记录的筛选和排序功能?(建议: 后续迭代)
