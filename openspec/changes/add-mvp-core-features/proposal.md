## Why

PetsPhoto 项目需要建立完整的 MVP（最小可行产品）基础设施，包括前端和后端的项目结构、核心功能规范和开发环境配置。这是项目的第一个里程碑，为后续的功能开发奠定基础。

当前状态：项目仅有 OpenSpec 文档，缺少实际的代码结构和功能实现。

目标：建立符合现代 Web 开发最佳实践的项目架构，使用 React + TypeScript (前端) 和 FastAPI + Python (后端)，并集成 shadcn/ui 设计系统。

## What Changes

本提案涵盖 MVP 阶段的所有核心功能和基础设施：

### 基础设施
- 前端项目初始化（Vite + React + TypeScript）
- 后端项目初始化（FastAPI + SQLAlchemy）
- shadcn/ui 组件库集成和主题配置
- 开发环境配置文件（`.env.example`, `docker-compose.yml`）
- 数据库模型和迁移脚本
- API 路由结构

### 核心功能
- **用户认证系统**：基于 Authentik 的 OIDC 认证，邮箱登录
- **图像上传管理**：支持拖拽上传、预览、验证
- **AI 图像生成**：集成 Veo3 API，支持预设风格
- **支付积分系统**：Stripe 支付集成，积分管理
- **UI 设计系统**：shadcn/ui 组件，简洁欧美风格

### 页面和路由
- 首页（Landing Page）
- 登录/注册页面
- 生成器页面（主要功能页）
- 个人资料页面
- 支付页面

## Impact

### 影响的规范（新增）
- `user-authentication` - 用户认证能力
- `image-upload` - 图像上传能力
- `ai-image-generation` - AI 图像生成能力
- `payment-credits` - 支付积分能力
- `ui-design-system` - UI 设计系统能力

### 影响的代码（新增）
```
frontend/               # 前端项目（全新创建）
├── src/
│   ├── components/
│   │   └── ui/        # shadcn/ui 组件
│   ├── pages/         # 页面组件
│   ├── services/      # API 调用
│   ├── hooks/         # 自定义 Hooks
│   ├── lib/           # 工具库
│   └── types/         # TypeScript 类型

backend/                # 后端项目（全新创建）
├── app/
│   ├── api/           # API 路由
│   ├── models/        # 数据库模型
│   ├── schemas/       # Pydantic 模式
│   ├── services/      # 业务逻辑
│   └── core/          # 核心配置
├── tests/             # 测试
└── alembic/           # 数据库迁移

docker-compose.yml      # Docker 编排（Authentik + 数据库）
.env.example           # 环境变量模板
```

### 外部依赖
- **Authentik**：用户认证服务（需要 Docker 部署）
- **Veo3 API**：AI 图像生成（需要 API Key）
- **Stripe**：支付处理（测试模式）

### 风险和注意事项
- 本提案包含大量新代码，建议分步实现和测试
- Authentik 需要本地 Docker 环境或云服务
- Veo3 API 可能需要申请访问权限
- 初期使用 SQLite，后续可能需要迁移到 PostgreSQL

### 不包含的内容（留待后续 Phase）
- Google OAuth 登录（Phase 2）
- 自定义风格描述（Phase 2）
- 用户历史记录（Phase 2）
- 即梦 API 集成（Phase 2）
- 性能优化和云存储（Phase 3）
