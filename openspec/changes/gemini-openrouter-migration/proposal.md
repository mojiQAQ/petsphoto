# Proposal: Gemini OpenRouter Migration

## Change ID
`gemini-openrouter-migration`

## Overview
将 Gemini 2.5 Flash 的访问方式从 Google Vertex AI 迁移到 OpenRouter，简化认证流程并降低集成复杂度。

### 当前状态
- 使用 Google Vertex AI API 访问 Gemini 模型
- 需要 Service Account JSON 或 Application Default Credentials
- 配置复杂：project_id, location, service_account_path 等多个参数
- OAuth2 token 刷新机制增加调试难度

### 目标状态
- 通过 OpenRouter API 访问 Gemini 2.5 Flash
- 仅需一个 API Key 即可调用
- 使用 OpenAI 兼容的 API 格式
- 简化环境变量配置

## Why

当前使用 Google Vertex AI 访问 Gemini 模型存在以下问题：
1. **认证复杂** - 需要 Service Account JSON 文件或 ADC 凭证
2. **配置繁琐** - 需要多个参数配合使用
3. **调试困难** - OAuth2 token 刷新机制增加故障排查难度

使用 OpenRouter 可以：
1. **简化认证** - 只需一个 API Key
2. **统一接口** - OpenAI 兼容格式，便于后续扩展
3. **降低门槛** - 无需 GCP 项目和服务账号配置

## Motivation
当前的 Google Vertex AI 集成方式对于快速开发和测试来说过于复杂。OpenRouter 提供了更简单的方式访问同样的 Gemini 模型，可以显著提升开发效率。

## Scope

### In Scope
- 新增 `OpenRouterClient` 图像生成客户端
- 添加 OpenRouter 相关环境变量配置
- 更新 `create_image_client` 工厂函数支持 `openrouter` provider
- 更新 `.env.example` 文档

### Out of Scope
- 移除现有 Google Vertex AI 客户端（保持向后兼容）
- 修改前端代码
- 修改其他 AI provider 实现

## Dependencies

- OpenRouter API Key (从 https://openrouter.ai/keys 获取)
- httpx (已有依赖)

## Risks

- **API 稳定性** - OpenRouter 作为中间层可能增加延迟
- **成本差异** - OpenRouter 的定价可能与直接调用 Google API 不同
- **功能限制** - 部分 Vertex AI 特有功能可能不可用

## Success Criteria

1. 可以通过 `IMAGE_PROVIDER=openrouter` 切换到 OpenRouter
2. 使用单个 API Key 完成图像生成
3. 现有 Google Vertex AI 方式仍然可用
