# Project Context

## Purpose

PetsPhoto 是一个宠物头像 AI 生成器，允许用户上传宠物照片，通过预设或自定义风格生成个性化的艺术头像。该项目旨在为宠物主人提供有趣、创意的宠物形象生成服务。

核心目标：
- 提供简单易用的宠物头像上传和生成功能
- 支持多种预设艺术风格和自定义风格描述
- 集成先进的 AI 图像生成技术（Veo3/即梦 3.1）
- 提供完整的用户账号和支付系统

## Tech Stack

### 前端
- **React 18+** - 现代化 UI 框架
- **TypeScript** - 类型安全的 JavaScript
- **Tailwind CSS 3** - 实用优先的 CSS 框架
- **shadcn/ui** - 高质量可定制 UI 组件库
- **Vite** - 快速的前端构建工具
- **React Router v6** - 客户端路由
- **TanStack Query (React Query)** - 服务器状态管理

### 后端
- **Python 3.10+** - 后端开发语言
- **FastAPI** - 现代异步 Web 框架
- **SQLite** - 轻量级关系数据库
- **SQLAlchemy** - Python ORM

### AI 图像生成
- **Veo3 API** - Google 的视频/图像生成模型
- **即梦 3.1 API** - 国内替代方案（备选）

### 认证与支付
- **Authentik** - 开源身份认证平台 (https://github.com/goauthentik/authentik)
  - Google OAuth 登录
  - 邮箱密码登录
- **Stripe** - 支付处理平台

## Project Conventions

### Code Style

#### 前端代码规范
- **命名规范**：
  - 组件：PascalCase（如 `ImageUploader.tsx`）
  - Hooks：camelCase with `use` prefix（如 `useImageGeneration.ts`）
  - 工具函数：camelCase（如 `formatImageUrl.ts`）
  - 常量：UPPER_SNAKE_CASE（如 `MAX_FILE_SIZE`）

- **文件组织**：
  ```
  src/
  ├── components/       # React 组件
  │   └── ui/          # shadcn/ui 组件
  ├── hooks/           # 自定义 Hooks
  ├── services/        # API 调用服务
  ├── utils/           # 工具函数
  ├── lib/             # 第三方库配置和工具
  ├── types/           # TypeScript 类型定义
  ├── pages/           # 页面组件
  └── assets/          # 静态资源
  ```

- **TypeScript 规范**：
  - 优先使用 `interface` 定义对象类型
  - 避免使用 `any`，使用 `unknown` 代替
  - 导出类型时使用 `export type` 或 `export interface`
  - 函数参数和返回值必须有类型注解

- **React 规范**：
  - 优先使用函数组件和 Hooks
  - 组件 props 必须定义 TypeScript 接口
  - 使用命名导出而非默认导出
  - 复杂状态逻辑使用自定义 Hooks

#### 后端代码规范
- **命名规范**：
  - 文件和模块：snake_case（如 `image_generator.py`）
  - 类：PascalCase（如 `ImageService`）
  - 函数和变量：snake_case（如 `generate_image`）
  - 常量：UPPER_SNAKE_CASE（如 `MAX_IMAGE_SIZE`）

- **文件组织**：
  ```
  backend/
  ├── app/
  │   ├── api/         # API 路由
  │   ├── models/      # 数据库模型
  │   ├── schemas/     # Pydantic 模式
  │   ├── services/    # 业务逻辑
  │   ├── core/        # 核心配置
  │   └── utils/       # 工具函数
  ├── tests/           # 测试文件
  └── alembic/         # 数据库迁移
  ```

- **Python 规范**：
  - 遵循 PEP 8 代码风格
  - 使用 Black 进行代码格式化
  - 使用 Pydantic 进行数据验证
  - 所有公共函数必须有 docstring
  - 类型注解使用 Python 3.10+ 语法

### UI Design Principles

#### 设计理念
- **简洁至上 (Minimalism First)**：去除不必要的装饰元素，专注于核心功能和内容
- **北欧/欧美风格**：大量留白、清晰的层次结构、优雅的排版
- **现代扁平化设计**：避免过度的阴影和渐变，使用细腻的边框和微妙的阴影
- **可访问性优先**：符合 WCAG 2.1 AA 标准，确保良好的对比度和键盘导航

#### 色彩系统
- **主色调**：
  - Primary: 现代蓝色或中性灰色系（如 Slate/Zinc）
  - 使用 shadcn/ui 默认主题作为基础
  - 支持浅色/深色模式切换

- **配色原则**：
  - 背景色：大量使用白色/浅灰色（浅色模式）或深灰色（深色模式）
  - 强调色：最多使用 1-2 种强调色，用于 CTA 按钮和重要操作
  - 文字：高对比度，确保可读性（灰度 700-900）
  - 边框：微妙的灰色边框（gray-200 在浅色模式）

- **色彩应用**：
  - 避免使用过于鲜艳的颜色
  - 使用渐进的灰度层次来区分不同的 UI 层级
  - 彩色仅用于状态指示（成功/警告/错误）和主要操作

#### 排版系统
- **字体**：
  - 西文：Inter / SF Pro / System UI（系统字体栈）
  - 中文：思源黑体 / PingFang SC / 微软雅黑（备选）
  - 代码/等宽：JetBrains Mono / Fira Code

- **字号层级**：
  - Heading 1: 2.5rem (40px) - 页面主标题
  - Heading 2: 2rem (32px) - 区块标题
  - Heading 3: 1.5rem (24px) - 卡片标题
  - Body: 1rem (16px) - 正文
  - Small: 0.875rem (14px) - 辅助文字
  - Tiny: 0.75rem (12px) - 标签、提示

- **字重**：
  - Regular (400) - 正文
  - Medium (500) - 强调文字
  - Semibold (600) - 小标题
  - Bold (700) - 大标题

- **行高**：
  - 标题：1.2-1.3
  - 正文：1.5-1.6
  - 确保良好的可读性

#### 间距系统
- **基于 Tailwind 的 4px 基准系统**：
  - 使用 4 的倍数：4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px
  - 页面边距：容器使用 px-4 (16px) 到 px-8 (32px)
  - 组件间距：使用 gap-4 到 gap-8
  - 内边距：按钮 px-4 py-2，卡片 p-6

#### UI 组件规范

##### shadcn/ui 组件使用
- **优先使用 shadcn/ui 组件**：
  - Button, Input, Card, Dialog, Dropdown Menu, Tabs, Toast
  - 根据项目需求定制 variant 和 size

- **组件定制原则**：
  - 修改 `tailwind.config.ts` 和 `globals.css` 中的 CSS 变量
  - 保持组件的可访问性特性（ARIA 属性）
  - 不要破坏组件的原有功能

##### 常用组件样式
- **按钮 (Button)**：
  - Primary: 填充背景，用于主要操作
  - Secondary: 边框样式，用于次要操作
  - Ghost: 无边框，用于辅助操作
  - 尺寸：sm, default, lg
  - 圆角：rounded-md (6px)

- **卡片 (Card)**：
  - 背景：白色（浅色模式）/ 深灰色（深色模式）
  - 边框：1px 细边框
  - 阴影：微妙的 shadow-sm，hover 时 shadow-md
  - 圆角：rounded-lg (8px)
  - 内边距：p-6

- **输入框 (Input)**：
  - 高度：h-10 (40px)
  - 边框：1px 边框，focus 时加粗或改变颜色
  - 圆角：rounded-md (6px)
  - 占位符：text-gray-400

- **对话框 (Dialog)**：
  - 遮罩：半透明黑色背景
  - 内容区：居中白色卡片，最大宽度 lg
  - 圆角：rounded-lg
  - 动画：淡入淡出

#### 布局规范
- **响应式设计**：
  - Mobile First 设计理念
  - 断点：sm (640px), md (768px), lg (1024px), xl (1280px)
  - 移动端：单列布局，堆叠显示
  - 桌面端：多列布局，利用水平空间

- **页面布局**：
  - 导航栏：固定在顶部，高度 64px
  - 主内容区：max-width-7xl 居中，左右留白
  - 底部：简洁的页脚信息

- **网格系统**：
  - 使用 Tailwind 的 grid 系统
  - 常用：grid-cols-1 md:grid-cols-2 lg:grid-cols-3
  - 间距：gap-4 到 gap-6

#### 交互设计
- **过渡动画**：
  - 使用 Tailwind 的 transition 工具类
  - 时长：150-300ms
  - 缓动：ease-in-out
  - 避免过度动画

- **加载状态**：
  - 按钮：loading spinner + 禁用状态
  - 页面：骨架屏（Skeleton）而非全屏 loading
  - 图片：渐进式加载，带占位符

- **反馈机制**：
  - 成功/错误：使用 Toast 通知（shadcn/ui Toast）
  - 表单验证：实时反馈，错误信息在输入框下方
  - 悬停状态：微妙的颜色变化或阴影增强

- **微交互**：
  - 按钮点击：轻微缩放效果
  - 卡片悬停：阴影加深
  - 图片悬停：轻微放大

#### 图标系统
- **图标库**：Lucide React（shadcn/ui 推荐）
- **尺寸**：
  - 小：16px (w-4 h-4)
  - 默认：20px (w-5 h-5)
  - 大：24px (w-6 h-6)
- **使用原则**：
  - 保持图标风格一致（全部使用 Lucide）
  - 图标与文字垂直居中对齐
  - 为图标添加适当的 aria-label

### Architecture Patterns

#### 前端架构
- **组件化设计**：功能独立、可复用的 React 组件
- **状态管理**：
  - 局部状态使用 `useState`/`useReducer`
  - 全局状态使用 Context API 或 Zustand（待定）
  - 服务器状态使用 TanStack Query (React Query)
- **API 调用**：统一的 API 服务层，使用 axios 或 fetch
- **路由**：React Router v6

#### 后端架构
- **分层架构**：
  - API Layer (FastAPI routes) - 处理 HTTP 请求
  - Service Layer - 业务逻辑
  - Repository Layer - 数据访问
  - Model Layer - 数据库模型

- **依赖注入**：使用 FastAPI 的 Depends 进行依赖注入

- **API 设计**：
  - RESTful API 设计原则
  - 使用 Pydantic 模式进行请求/响应验证
  - 统一的错误处理和响应格式

#### 数据库设计
- **ORM**：使用 SQLAlchemy
- **迁移**：使用 Alembic 进行数据库迁移
- **关系设计**：
  - User - 用户表
  - Image - 生成的图片记录
  - Transaction - 支付交易记录
  - GenerationStyle - 风格模板（可选）

### Testing Strategy

#### 前端测试
- **单元测试**：
  - 框架：Vitest
  - 组件测试：React Testing Library
  - 工具函数测试覆盖率 > 80%

- **E2E 测试**（后期）：
  - 框架：Playwright 或 Cypress
  - 覆盖关键用户流程

#### 后端测试
- **单元测试**：
  - 框架：pytest
  - 覆盖率目标 > 80%
  - 测试所有 service 和 util 函数

- **集成测试**：
  - API 端点测试
  - 数据库操作测试
  - 使用 TestClient (FastAPI)

- **API 测试**：
  - 使用 pytest-asyncio 测试异步代码
  - Mock 外部 API 调用（Veo3、Stripe）

### Git Workflow

- **分支策略**：
  - `main` - 生产环境代码
  - `develop` - 开发分支
  - `feature/*` - 功能分支
  - `bugfix/*` - 错误修复分支
  - `hotfix/*` - 紧急修复分支

- **提交规范**：遵循 Conventional Commits
  ```
  feat: 新功能
  fix: 错误修复
  docs: 文档更新
  style: 代码格式化
  refactor: 重构
  test: 测试相关
  chore: 构建/工具链更新
  ```

- **合并策略**：
  - Feature 分支合并到 develop 使用 Squash and Merge
  - Develop 合并到 main 使用 Merge Commit
  - 所有 PR 需要 code review

## Domain Context

### 图像生成流程
1. **上传阶段**：用户上传宠物照片（支持 JPG、PNG，最大 10MB）
2. **风格选择**：用户选择预设风格或输入自定义风格描述
3. **生成请求**：后端调用 Veo3/即梦 API 生成图像
4. **结果展示**：前端展示生成的图片，支持下载和再次生成

### 用户认证流程
- 使用 Authentik 作为身份提供商（IdP）
- 支持 OAuth 2.0 + OpenID Connect
- 前端通过 Authentik 获取 access token
- 后端验证 token 并识别用户身份

### 支付流程
- 使用 Stripe Checkout 进行支付
- 积分制：用户购买积分，每次生成消耗一定积分
- Webhook 处理支付成功/失败事件

### AI 模型选择
- **主要**：Veo3 API（Google）
  - 优点：高质量、稳定
  - 缺点：可能需要 VPN，成本较高

- **备选**：即梦 3.1 API（国内）
  - 优点：国内访问快，成本较低
  - 缺点：质量可能稍逊

## Important Constraints

### 技术约束
- **前端**：必须支持 Chrome、Safari、Firefox 最新两个版本
- **后端**：Python 3.10+ 运行环境
- **数据库**：初期使用 SQLite，用户量增长后考虑迁移到 PostgreSQL
- **文件存储**：初期本地存储，后期考虑 S3/OSS

### 业务约束
- **图片生成**：单次生成时间不超过 30 秒
- **文件大小**：上传图片不超过 10MB
- **用户体验**：首屏加载时间 < 3 秒
- **成本控制**：每次生成成本控制在合理范围

### 合规约束
- **数据隐私**：符合 GDPR 和国内隐私保护法规
- **支付安全**：PCI DSS 合规（由 Stripe 保证）
- **内容审核**：生成内容需符合社区规范，避免不当内容

### 扩展性约束
- **初期目标**：支持 100 并发用户
- **数据库**：单表记录数 < 100 万时使用 SQLite
- **API 限流**：防止滥用，每用户每分钟最多 10 次请求

## External Dependencies

### 核心外部服务

#### 1. Authentik (身份认证)
- **用途**：用户注册、登录、OAuth
- **集成方式**：OpenID Connect (OIDC)
- **部署方式**：Docker 自托管或 Cloud 版本
- **文档**：https://goauthentik.io/docs/

#### 2. Veo3 API (主要图像生成)
- **用途**：AI 图像生成
- **API 类型**：REST API
- **认证方式**：API Key
- **文档**：Google AI Platform 文档
- **限流**：待确认（根据 API 文档）

#### 3. 即梦 3.1 API (备选图像生成)
- **用途**：AI 图像生成（国内备选）
- **API 类型**：REST API
- **认证方式**：API Key
- **文档**：即梦官方文档
- **限流**：待确认

#### 4. Stripe (支付处理)
- **用途**：信用卡支付、订阅管理
- **集成方式**：Stripe Checkout + Webhooks
- **SDK**：stripe-python (后端)、@stripe/stripe-js (前端)
- **文档**：https://stripe.com/docs
- **测试模式**：开发阶段使用 Test Mode

### 可选外部服务
- **对象存储**（后期）：AWS S3 / 阿里云 OSS / Cloudflare R2
- **CDN**（后期）：Cloudflare / AWS CloudFront
- **监控和日志**：Sentry (错误跟踪)、LogTail (日志)
- **邮件服务**：SendGrid / AWS SES (用户通知)

### 开发工具和服务
- **版本控制**：GitHub
- **CI/CD**：GitHub Actions
- **包管理**：npm (前端)、pip (后端)
- **代码质量**：ESLint + Prettier (前端)、Black + Ruff (后端)

## Environment Configuration

### 环境变量管理
- 使用 `.env` 文件（不提交到 Git）
- 提供 `.env.example` 模板文件
- 生产环境使用环境变量或密钥管理服务

### 必需环境变量
```bash
# 后端
DATABASE_URL=sqlite:///./petsphoto.db
SECRET_KEY=your-secret-key
AUTHENTIK_CLIENT_ID=xxx
AUTHENTIK_CLIENT_SECRET=xxx
AUTHENTIK_DOMAIN=https://auth.yourapp.com
VEO3_API_KEY=xxx
JIMENG_API_KEY=xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# 前端
VITE_API_BASE_URL=http://localhost:8000
VITE_AUTHENTIK_DOMAIN=https://auth.yourapp.com
VITE_STRIPE_PUBLIC_KEY=pk_test_xxx
VITE_APP_NAME=PetsPhoto
VITE_THEME_MODE=light  # light | dark | system
```

## Development Setup

### 前端开发
```bash
cd frontend
npm install

# 初始化 shadcn/ui（首次设置）
npx shadcn-ui@latest init

# 添加需要的组件（示例）
npx shadcn-ui@latest add button card input dialog toast

npm run dev        # 开发服务器：http://localhost:5173
npm run build      # 生产构建
npm run test       # 运行测试
npm run lint       # 代码检查
```

### 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload  # 开发服务器：http://localhost:8000
pytest                          # 运行测试
black .                         # 代码格式化
```

### Authentik 本地开发
```bash
docker-compose -f docker-compose.authentik.yml up -d
# 访问 http://localhost:9000 进行配置
```

## Page Structure and Layouts

### 主要页面布局

#### 1. 首页 (Landing Page)
- **Hero 区域**：
  - 大标题 + 简短描述（居中对齐）
  - 主要 CTA 按钮："开始创作"
  - 示例图片展示（3-4 张生成示例，Grid 布局）

- **功能介绍**：
  - 3 列卡片布局（移动端堆叠）
  - 图标 + 标题 + 描述
  - 功能：上传、选择风格、生成

- **定价信息**：
  - 简洁的定价卡片
  - 积分套餐展示

- **页脚**：
  - 链接：关于、隐私政策、服务条款
  - 社交媒体图标

#### 2. 生成器页面 (Generator Page)
- **左侧面板**（桌面端）/ **顶部区域**（移动端）：
  - 上传区域（大而明显的拖拽区）
  - 已上传图片预览
  - 清除/重新上传按钮

- **右侧面板**（桌面端）/ **中部区域**（移动端）：
  - 风格选择器：
    - Tab: "预设风格" vs "自定义风格"
    - 预设风格：网格卡片布局（2-3 列）
    - 自定义风格：Textarea 输入框
  - 生成按钮（固定在底部，明显突出）

- **结果区域**（生成后显示）：
  - 全宽或 Dialog 模式显示生成结果
  - 图片预览（大图）
  - 操作按钮：下载、重新生成、分享

#### 3. 历史记录页面 (Gallery Page)
- **顶部筛选栏**：
  - 搜索框
  - 排序选项（最新、最旧、最受欢迎）
  - 视图切换（网格/列表）

- **图片网格**：
  - 响应式网格：1 列（移动）→ 2 列（平板）→ 3-4 列（桌面）
  - 每个卡片：缩略图 + 创建时间 + 操作按钮
  - 悬停效果：显示更多操作

- **图片详情 Dialog**：
  - 大图展示
  - 元数据：生成时间、使用风格
  - 操作：下载、删除、重新生成

#### 4. 个人资料页面 (Profile Page)
- **用户信息卡片**：
  - 头像 + 用户名 + 邮箱
  - 编辑按钮

- **积分余额**：
  - 大号显示当前积分
  - 购买积分按钮
  - 使用历史（折叠面板）

- **账户设置**：
  - 密码修改
  - 主题偏好
  - 通知设置

#### 5. 支付页面 (Payment Page)
- **积分套餐选择**：
  - 3-4 个套餐卡片（并排或堆叠）
  - 推荐标签（"Most Popular"）
  - 价格 + 积分数量
  - 立即购买按钮

- **支付方式**：
  - Stripe Checkout（跳转到 Stripe 托管页面）
  - 或 Stripe Elements（内嵌表单）

#### 6. 登录/注册页面 (Auth Pages)
- **居中卡片设计**：
  - 背景：渐变或纯色
  - 卡片：白色背景、阴影、居中

- **表单**：
  - 简洁的输入框（邮箱、密码）
  - 记住我复选框
  - 主要 CTA 按钮
  - 分隔线 + "或使用其他方式登录"
  - OAuth 按钮（Google）

- **切换链接**：
  - "还没有账号？注册"
  - "忘记密码？"

### 通用 UI 元素

#### 导航栏 (Navbar)
- **Logo**（左侧）：文字或图标
- **导航链接**（中间）：首页、生成器、历史
- **用户菜单**（右侧）：
  - 未登录：登录/注册按钮
  - 已登录：积分显示 + 头像 Dropdown
    - 个人资料
    - 设置
    - 退出登录
- **主题切换**：太阳/月亮图标
- **移动端**：汉堡菜单

#### 加载状态
- **骨架屏 (Skeleton)**：
  - 用于图片网格加载
  - 用于卡片内容加载

- **Spinner**：
  - 按钮内的 loading 状态
  - 页面级别加载（少用）

- **进度条**：
  - 文件上传进度
  - AI 生成进度（估算）

#### 空状态 (Empty State)
- **图标 + 文字提示**：
  - 历史记录为空："还没有生成记录，开始创作吧！"
  - 上传区域：拖拽图标 + "拖拽或点击上传图片"

## Project Milestones

### Phase 1: MVP (最小可行产品)
- **UI 基础设施**：
  - shadcn/ui 初始化和主题配置
  - 响应式导航栏（移动端汉堡菜单）
  - 浅色/深色模式切换
  - 基础页面布局和路由
- **用户认证**：
  - 邮箱登录页面（简洁表单设计）
  - 注册页面
  - 密码重置流程
- **图片上传功能**：
  - 拖拽上传区域（大而明显）
  - 图片预览（带编辑/删除功能）
  - 上传进度指示
- **风格选择**：
  - 预设风格卡片展示（3-5 种）
  - 卡片 hover 效果
  - 选中状态视觉反馈
- **AI 图像生成**：
  - Veo3 API 集成
  - 生成进度指示（骨架屏）
  - 结果展示（大图预览）
  - 下载按钮
- **支付系统**：
  - 积分显示（导航栏）
  - 购买积分页面（Stripe Checkout）
  - 支付成功/失败提示

### Phase 2: 功能增强
- **增强认证**：
  - Google OAuth 登录（shadcn/ui Button + Google 图标）
  - 用户个人资料页面
- **自定义风格**：
  - 文本输入框用于风格描述
  - 风格提示词建议（Dropdown）
  - 保存自定义风格模板
- **历史记录**：
  - 用户生成历史画廊（Grid 布局）
  - 图片详情页（Dialog）
  - 删除/重新生成功能
- **分享功能**：
  - 图片下载（多种尺寸）
  - 社交分享按钮
  - 复制链接功能
- **备选 AI**：
  - 即梦 API 集成
  - AI 提供商选择（Tabs）

### Phase 3: 优化和扩展
- **性能优化**：
  - 图片懒加载和优化
  - 代码分割和懒加载
  - PWA 支持
- **云存储**：
  - 对象存储集成（S3/OSS）
  - CDN 加速
- **高级付费功能**：
  - 订阅制付费模式（Stripe Subscriptions）
  - 套餐选择页面（定价表格）
- **移动端优化**：
  - 移动端专属布局调整
  - 触摸手势支持
  - 原生分享 API
- **社交功能**：
  - 公开画廊（社区作品展示）
  - 点赞/收藏功能
  - 评论系统
