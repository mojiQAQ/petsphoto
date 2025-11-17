## 1. 项目初始化

- [x] 1.1 创建前端项目
  - [x] 1.1.1 使用 Vite 创建 React + TypeScript 项目
  - [x] 1.1.2 安装核心依赖（React Router, TanStack Query）
  - [x] 1.1.3 配置 Tailwind CSS
  - [x] 1.1.4 初始化 shadcn/ui
  - [ ] 1.1.5 安装 shadcn/ui 核心组件（Button, Card, Input, Dialog, Toast, etc.）
  - [x] 1.1.6 安装 Lucide React 图标库
  - [x] 1.1.7 配置目录结构（components, pages, services, hooks, lib, types）
  - [x] 1.1.8 配置 ESLint 和 Prettier
  - [x] 1.1.9 创建 `.env.example` 文件

- [x] 1.2 创建后端项目
  - [x] 1.2.1 创建 FastAPI 项目结构
  - [x] 1.2.2 安装核心依赖（FastAPI, SQLAlchemy, Alembic, Pydantic）
  - [x] 1.2.3 安装外部集成依赖（Stripe, 图片处理库）
  - [x] 1.2.4 配置目录结构（api, models, schemas, services, core, utils）
  - [x] 1.2.5 创建 `requirements.txt`
  - [x] 1.2.6 配置 Black 和 Ruff
  - [x] 1.2.7 创建 `.env.example` 文件

- [x] 1.3 Docker 和开发环境
  - [x] 1.3.1 创建 `docker-compose.yml`（Authentik + PostgreSQL）
  - [x] 1.3.2 配置 Authentik 服务
  - [x] 1.3.3 创建项目根目录 README.md

## 2. UI 设计系统实现

- [x] 2.1 主题配置
  - [x] 2.1.1 配置 shadcn/ui 主题（CSS 变量）
  - [x] 2.1.2 创建 ThemeProvider 组件
  - [x] 2.1.3 实现浅色/深色模式切换
  - [ ] 2.1.4 配置字体（Inter + 中文字体）

- [x] 2.2 布局组件
  - [x] 2.2.1 创建 Navbar 组件（响应式）
  - [x] 2.2.2 创建 Footer 组件
  - [x] 2.2.3 创建 Container 组件
  - [x] 2.2.4 创建 Layout 组件（组合 Navbar + Footer）

- [ ] 2.3 通用组件
  - [ ] 2.3.1 创建 ImageUploader 组件
  - [ ] 2.3.2 创建 StyleCard 组件（风格选择卡片）
  - [ ] 2.3.3 创建 LoadingSpinner 组件
  - [ ] 2.3.4 创建 EmptyState 组件
  - [ ] 2.3.5 创建 CreditsDisplay 组件（积分显示）

## 3. 用户认证系统

- [ ] 3.1 Authentik 配置
  - [ ] 3.1.1 启动 Authentik Docker 容器
  - [ ] 3.1.2 在 Authentik 中创建 Application 和 Provider
  - [ ] 3.1.3 配置 OIDC 参数（client ID, secret, redirect URI）

- [ ] 3.2 后端认证实现
  - [ ] 3.2.1 创建 User 数据库模型
  - [ ] 3.2.2 实现 Authentik OIDC 集成
  - [ ] 3.2.3 实现 JWT token 验证中间件
  - [ ] 3.2.4 创建认证相关 API 端点（/api/auth/*）
  - [ ] 3.2.5 实现用户注册逻辑
  - [ ] 3.2.6 实现用户登录逻辑
  - [ ] 3.2.7 实现密码重置逻辑
  - [ ] 3.2.8 实现 token 刷新逻辑

- [ ] 3.3 前端认证实现
  - [ ] 3.3.1 创建 AuthContext 和 AuthProvider
  - [ ] 3.3.2 实现 useAuth Hook
  - [ ] 3.3.3 创建登录页面（Login.tsx）
  - [ ] 3.3.4 创建注册页面（Register.tsx）
  - [ ] 3.3.5 创建密码重置页面
  - [ ] 3.3.6 实现受保护路由（ProtectedRoute 组件）
  - [ ] 3.3.7 实现 token 自动刷新
  - [ ] 3.3.8 实现登出功能

## 4. 图像上传功能

- [ ] 4.1 后端上传实现
  - [ ] 4.1.1 创建 UploadedImage 数据库模型
  - [ ] 4.1.2 实现文件上传 API（/api/images/upload）
  - [ ] 4.1.3 实现文件验证（类型、大小、尺寸）
  - [ ] 4.1.4 实现临时文件存储逻辑
  - [ ] 4.1.5 实现文件清理定时任务

- [ ] 4.2 前端上传实现
  - [ ] 4.2.1 创建 ImageUploadZone 组件（拖拽上传）
  - [ ] 4.2.2 实现文件选择功能
  - [ ] 4.2.3 实现客户端文件验证
  - [ ] 4.2.4 实现上传进度显示
  - [ ] 4.2.5 实现图片预览功能
  - [ ] 4.2.6 实现图片删除功能
  - [ ] 4.2.7 创建 useImageUpload Hook

## 5. AI 图像生成功能

- [ ] 5.1 后端生成实现
  - [ ] 5.1.1 创建 GenerationJob 数据库模型
  - [ ] 5.1.2 创建 GenerationStyle 数据库模型（或配置文件）
  - [ ] 5.1.3 集成 Veo3 API
  - [ ] 5.1.4 实现生成任务创建 API（/api/generate）
  - [ ] 5.1.5 实现生成任务状态查询 API
  - [ ] 5.1.6 实现生成队列管理
  - [ ] 5.1.7 实现生成结果存储
  - [ ] 5.1.8 实现积分扣除逻辑
  - [ ] 5.1.9 实现风格列表 API（/api/styles）

- [ ] 5.2 前端生成实现
  - [ ] 5.2.1 创建 StyleSelector 组件（风格选择）
  - [ ] 5.2.2 创建 Generator 页面
  - [ ] 5.2.3 实现生成请求逻辑
  - [ ] 5.2.4 实现生成进度轮询
  - [ ] 5.2.5 创建 GenerationResult Dialog 组件
  - [ ] 5.2.6 实现图片下载功能
  - [ ] 5.2.7 实现重新生成功能
  - [ ] 5.2.8 创建 useImageGeneration Hook

## 6. 支付积分系统

- [ ] 6.1 Stripe 配置
  - [ ] 6.1.1 创建 Stripe 账号（测试模式）
  - [ ] 6.1.2 获取 API Keys
  - [ ] 6.1.3 配置 Stripe Webhook

- [ ] 6.2 后端支付实现
  - [ ] 6.2.1 创建 CreditPackage 数据库模型
  - [ ] 6.2.2 创建 CreditTransaction 数据库模型
  - [ ] 6.2.3 创建 StripeEvent 数据库模型
  - [ ] 6.2.4 集成 Stripe SDK
  - [ ] 6.2.5 实现支付会话创建 API（/api/credits/purchase）
  - [ ] 6.2.6 实现 Webhook 处理（/api/webhooks/stripe）
  - [ ] 6.2.7 实现积分余额查询 API
  - [ ] 6.2.8 实现交易历史 API
  - [ ] 6.2.9 实现积分套餐列表 API

- [ ] 6.3 前端支付实现
  - [ ] 6.3.1 创建 Payment 页面
  - [ ] 6.3.2 创建 CreditPackageCard 组件
  - [ ] 6.3.3 实现 Stripe Checkout 跳转
  - [ ] 6.3.4 创建支付成功页面
  - [ ] 6.3.5 创建支付取消页面
  - [ ] 6.3.6 实现积分余额显示（Navbar）
  - [ ] 6.3.7 创建积分不足提示

## 7. 页面和路由

- [ ] 7.1 创建首页（Landing Page）
  - [ ] 7.1.1 Hero 区域
  - [ ] 7.1.2 功能介绍区域
  - [ ] 7.1.3 定价区域
  - [ ] 7.1.4 页脚

- [ ] 7.2 创建生成器页面
  - [ ] 7.2.1 左侧上传区域
  - [ ] 7.2.2 右侧风格选择区域
  - [ ] 7.2.3 生成按钮
  - [ ] 7.2.4 结果展示

- [ ] 7.3 创建个人资料页面
  - [ ] 7.3.1 用户信息卡片
  - [ ] 7.3.2 积分余额显示
  - [ ] 7.3.3 账户设置

- [ ] 7.4 配置路由
  - [ ] 7.4.1 创建 Router 配置
  - [ ] 7.4.2 配置受保护路由
  - [ ] 7.4.3 配置 404 页面

## 8. 数据库和迁移

- [x] 8.1 数据库初始化
  - [x] 8.1.1 配置 SQLAlchemy
  - [x] 8.1.2 创建所有数据库模型
  - [x] 8.1.3 配置 Alembic
  - [ ] 8.1.4 创建初始迁移脚本
  - [ ] 8.1.5 运行迁移

- [x] 8.2 种子数据
  - [x] 8.2.1 创建预设风格数据
  - [x] 8.2.2 创建积分套餐数据
  - [ ] 8.2.3 创建测试用户（开发环境）

## 9. 测试

- [ ] 9.1 后端测试
  - [ ] 9.1.1 测试用户认证流程
  - [ ] 9.1.2 测试图片上传功能
  - [ ] 9.1.3 测试生成功能（Mock Veo3 API）
  - [ ] 9.1.4 测试支付功能（Stripe 测试模式）
  - [ ] 9.1.5 测试 Webhook 处理

- [ ] 9.2 前端测试
  - [ ] 9.2.1 测试认证流程（登录/注册）
  - [ ] 9.2.2 测试图片上传 UI
  - [ ] 9.2.3 测试风格选择和生成
  - [ ] 9.2.4 测试支付流程
  - [ ] 9.2.5 测试响应式布局（移动端/桌面端）

## 10. 文档和部署准备

- [ ] 10.1 文档
  - [ ] 10.1.1 更新 README.md（安装和运行说明）
  - [ ] 10.1.2 创建 API 文档（FastAPI 自动生成）
  - [ ] 10.1.3 创建开发者文档

- [ ] 10.2 部署准备
  - [ ] 10.2.1 配置生产环境变量
  - [ ] 10.2.2 优化前端构建
  - [ ] 10.2.3 配置 CORS
  - [ ] 10.2.4 配置日志系统
  - [ ] 10.2.5 配置错误监控（Sentry）

## 11. 优化和收尾

- [ ] 11.1 性能优化
  - [ ] 11.1.1 前端代码分割
  - [ ] 11.1.2 图片懒加载
  - [ ] 11.1.3 API 响应缓存

- [ ] 11.2 安全加固
  - [ ] 11.2.1 检查所有 API 端点的认证
  - [ ] 11.2.2 实现 Rate Limiting
  - [ ] 11.2.3 SQL 注入防护
  - [ ] 11.2.4 XSS 防护

- [ ] 11.3 用户体验
  - [ ] 11.3.1 添加 Loading 状态
  - [ ] 11.3.2 添加错误处理和提示
  - [ ] 11.3.3 优化表单验证体验
  - [ ] 11.3.4 添加 Toast 通知

- [ ] 11.4 最终检查
  - [ ] 11.4.1 检查所有页面的响应式设计
  - [ ] 11.4.2 检查浅色/深色模式
  - [ ] 11.4.3 检查无障碍性
  - [ ] 11.4.4 浏览器兼容性测试
