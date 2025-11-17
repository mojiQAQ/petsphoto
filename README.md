# PetsPhoto - AI 宠物头像生成器

PetsPhoto 是一个基于 AI 的宠物头像生成器，用户可以上传宠物照片，选择预设风格或自定义风格描述，通过 AI 生成个性化的艺术头像。

## 技术栈

### 前端
- **React 18+** with TypeScript
- **Vite** - 快速构建工具
- **Tailwind CSS 3** - 实用优先的 CSS 框架
- **shadcn/ui** - 高质量 UI 组件库
- **React Router v6** - 路由管理
- **TanStack Query** - 服务器状态管理
- **Lucide React** - 图标库

### 后端
- **Python 3.10+**
- **FastAPI** - 现代异步 Web 框架
- **SQLite** - 轻量级数据库
- **SQLAlchemy** - ORM
- **Alembic** - 数据库迁移

### 外部服务
- **Authentik** - 身份认证平台
- **Veo3 API** - AI 图像生成
- **Stripe** - 支付处理

## 项目结构

```
petsphoto/
├── frontend/               # React 前端项目
│   ├── src/
│   │   ├── components/    # React 组件
│   │   │   └── ui/       # shadcn/ui 组件
│   │   ├── pages/        # 页面组件
│   │   ├── services/     # API 调用
│   │   ├── hooks/        # 自定义 Hooks
│   │   ├── lib/          # 工具库
│   │   └── types/        # TypeScript 类型
│   └── package.json
├── backend/               # FastAPI 后端项目
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── models/       # 数据库模型
│   │   ├── schemas/      # Pydantic 模式
│   │   ├── services/     # 业务逻辑
│   │   ├── core/         # 核心配置
│   │   └── utils/        # 工具函数
│   ├── tests/            # 测试
│   └── requirements.txt
├── docker-compose.yml    # Docker 编排文件
├── .env.docker          # Docker 环境变量
└── README.md            # 项目文档
```

## 快速开始

### 前置要求

- Node.js 18+ 和 npm
- Python 3.10+
- Docker 和 Docker Compose (用于 Authentik)

### 1. 克隆项目

```bash
git clone <repository-url>
cd petsphoto
```

### 2. 启动 Authentik 服务

```bash
# 复制环境变量文件
cp .env.docker .env

# 生成安全的 Authentik Secret Key
python -c "import secrets; print(secrets.token_urlsafe(50))"
# 将生成的密钥替换到 .env 中的 AUTHENTIK_SECRET_KEY

# 启动 Authentik
docker-compose up -d

# 访问 http://localhost:9000 进行初始配置
```

### 3. 配置 Authentik

1. 访问 http://localhost:9000/if/flow/initial-setup/
2. 创建管理员账号
3. 登录后，创建 Application 和 Provider:
   - 进入 Applications > Create
   - 选择 Provider Type: OAuth2/OpenID Provider
   - 配置 Redirect URIs: `http://localhost:5173/auth/callback`
   - 复制 Client ID 和 Client Secret

### 4. 配置后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，填写必要的配置：
# - SECRET_KEY (生成: openssl rand -hex 32)
# - AUTHENTIK_CLIENT_ID (从 Authentik 获取)
# - AUTHENTIK_CLIENT_SECRET (从 Authentik 获取)
# - VEO3_API_KEY (从 Veo3 获取)
# - STRIPE_SECRET_KEY (从 Stripe 获取，测试模式)
# - STRIPE_WEBHOOK_SECRET (从 Stripe 获取)

# 运行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将运行在 http://localhost:8000

API 文档可在 http://localhost:8000/docs 访问

### 5. 配置前端

```bash
cd frontend

# 安装依赖
npm install

# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，填写：
# - VITE_AUTHENTIK_CLIENT_ID (与后端相同)
# - VITE_STRIPE_PUBLIC_KEY (Stripe 公钥)

# 启动开发服务器
npm run dev
```

前端将运行在 http://localhost:5173

## 开发指南

### 前端开发

```bash
cd frontend

# 开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 代码检查
npm run lint

# 代码格式化
npm run format
```

### 后端开发

```bash
cd backend

# 运行开发服务器
uvicorn app.main:app --reload

# 代码格式化
black .
ruff check .

# 运行测试
pytest

# 创建数据库迁移
alembic revision --autogenerate -m "description"

# 应用迁移
alembic upgrade head
```

## 功能特性

### MVP 阶段 (当前)
- ✅ 用户认证（邮箱登录，基于 Authentik）
- ✅ 图片上传（拖拽上传，预览）
- ✅ AI 图像生成（预设风格）
- ✅ 支付积分系统（Stripe）
- ✅ 响应式 UI（shadcn/ui）

### Phase 2 (计划中)
- ⬜ Google OAuth 登录
- ⬜ 自定义风格描述
- ⬜ 用户生成历史
- ⬜ 即梦 API 集成（备选）

### Phase 3 (未来)
- ⬜ 云存储集成 (S3/OSS)
- ⬜ CDN 加速
- ⬜ 高级订阅功能
- ⬜ 社区功能

## 环境变量说明

### 后端 (.env)

| 变量名 | 说明 | 必需 |
|--------|------|------|
| SECRET_KEY | JWT 密钥 (min 32 chars) | ✅ |
| DATABASE_URL | 数据库连接字符串 | ✅ |
| AUTHENTIK_CLIENT_ID | Authentik 客户端 ID | ✅ |
| AUTHENTIK_CLIENT_SECRET | Authentik 客户端密钥 | ✅ |
| VEO3_API_KEY | Veo3 API 密钥 | ✅ |
| STRIPE_SECRET_KEY | Stripe 密钥 | ✅ |
| STRIPE_WEBHOOK_SECRET | Stripe Webhook 密钥 | ✅ |

### 前端 (.env)

| 变量名 | 说明 | 必需 |
|--------|------|------|
| VITE_API_BASE_URL | 后端 API 地址 | ✅ |
| VITE_AUTHENTIK_DOMAIN | Authentik 域名 | ✅ |
| VITE_AUTHENTIK_CLIENT_ID | Authentik 客户端 ID | ✅ |
| VITE_STRIPE_PUBLIC_KEY | Stripe 公钥 | ✅ |

## 测试

### 测试 Stripe 支付

使用 Stripe 测试卡号：
- **成功支付**: 4242 4242 4242 4242
- **失败支付**: 4000 0000 0000 0002
- **需要 3D 验证**: 4000 0027 6000 3184

任意未来日期作为过期日期，任意 3 位数作为 CVC。

## 部署

(待补充)

## 许可证

(待定义)

## 联系方式

(待补充)
