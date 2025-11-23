# Design: Supabase Authentication Integration

## Architecture Overview

### Current Architecture
```
┌─────────┐         ┌─────────┐         ┌──────────┐
│ Browser │ ◄─────► │ Backend │ ◄─────► │ Database │
└─────────┘         └─────────┘         └──────────┘
     │                    │
     │                    ├─ Generate JWT
     │                    ├─ Verify JWT
     │                    └─ Hash Password
     │
     └─ Store JWT in localStorage
```

### New Architecture
```
┌─────────┐         ┌──────────┐         ┌─────────┐         ┌──────────┐
│ Browser │ ◄─────► │ Supabase │         │ Backend │ ◄─────► │ Database │
└─────────┘         │   Auth   │         └─────────┘         └──────────┘
     │              └──────────┘               │
     │                    │                    │
     ├─ Supabase SDK     │                    ├─ Verify Supabase JWT
     ├─ Get JWT          │                    ├─ Sync User Data
     └─ OAuth Flow       │                    └─ Manage User Resources
                         │
                         └─ Issue JWT Token
```

## Component Design

### 1. Frontend: Supabase Client Setup

#### 文件: `src/lib/supabase.ts`
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    storage: window.localStorage,
  },
})

// 类型定义
export type SupabaseUser = {
  id: string
  email: string
  user_metadata: {
    full_name?: string
    avatar_url?: string
  }
}
```

### 2. Frontend: Auth Context Refactor

#### 文件: `src/contexts/AuthContext.tsx`
```typescript
import { createContext, useContext, useEffect, useState } from 'react'
import { supabase, SupabaseUser } from '@/lib/supabase'
import { User as AppUser } from '@/types/auth'
import { syncUserWithBackend } from '@/services/auth'

interface AuthContextType {
  user: AppUser | null
  supabaseUser: SupabaseUser | null
  isLoading: boolean
  isAuthenticated: boolean
  signInWithEmail: (email: string, password: string) => Promise<void>
  signUpWithEmail: (email: string, password: string, fullName?: string) => Promise<void>
  signInWithGoogle: () => Promise<void>
  signInWithGithub: () => Promise<void>
  signOut: () => Promise<void>
  getAccessToken: () => Promise<string | null>
}

// 实现略...
```

**关键逻辑**:
1. 监听 `supabase.auth.onAuthStateChange()` 事件
2. 当用户登录时，获取 JWT 并同步到后端
3. 存储 Supabase session 和本地用户数据
4. 提供便捷的登录方法（邮箱、Google、GitHub）

### 3. Frontend: Login Page with OAuth

#### 文件: `src/pages/LoginPage.tsx`
```typescript
// 登录页面添加 OAuth 按钮
<div className="space-y-3">
  <Button
    onClick={() => signInWithGoogle()}
    variant="outline"
    className="w-full"
  >
    <FcGoogle className="mr-2 h-5 w-5" />
    使用 Google 登录
  </Button>

  <Button
    onClick={() => signInWithGithub()}
    variant="outline"
    className="w-full"
  >
    <FaGithub className="mr-2 h-5 w-5" />
    使用 GitHub 登录
  </Button>
</div>

<div className="relative my-4">
  <div className="absolute inset-0 flex items-center">
    <span className="w-full border-t" />
  </div>
  <div className="relative flex justify-center text-xs uppercase">
    <span className="bg-background px-2 text-muted-foreground">
      或使用邮箱登录
    </span>
  </div>
</div>

{/* 邮箱登录表单 */}
```

### 4. Backend: JWT Verification Middleware

#### 文件: `app/core/supabase.py`
```python
from jose import jwt, JWTError
import httpx
from functools import lru_cache
from app.core.config import settings

class SupabaseJWTVerifier:
    """Supabase JWT 验证器"""

    def __init__(self):
        self.jwks_uri = f"{settings.SUPABASE_URL}/auth/v1/jwks"
        self.issuer = f"{settings.SUPABASE_URL}/auth/v1"
        self._jwks_cache = None

    @lru_cache(maxsize=1)
    async def get_jwks(self):
        """获取 Supabase JWKS (JSON Web Key Set)"""
        async with httpx.AsyncClient() as client:
            response = await client.get(self.jwks_uri)
            response.raise_for_status()
            return response.json()

    async def verify_token(self, token: str) -> dict:
        """验证 Supabase JWT token"""
        try:
            jwks = await self.get_jwks()

            # 验证 JWT
            payload = jwt.decode(
                token,
                jwks,
                algorithms=["RS256"],
                audience="authenticated",
                issuer=self.issuer,
            )

            return payload
        except JWTError as e:
            raise ValueError(f"Invalid token: {e}")

# 单例
supabase_verifier = SupabaseJWTVerifier()
```

### 5. Backend: Updated Dependencies

#### 文件: `app/api/deps.py`
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.supabase import supabase_verifier
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户 (从 Supabase JWT)"""
    token = credentials.credentials

    try:
        # 验证 Supabase JWT
        payload = await supabase_verifier.verify_token(token)
        supabase_user_id = payload.get("sub")
        email = payload.get("email")

        if not supabase_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        # 从数据库获取用户
        user = db.query(User).filter(
            User.supabase_user_id == supabase_user_id
        ).first()

        if not user:
            # 用户不存在，自动创建
            user = User(
                supabase_user_id=supabase_user_id,
                email=email,
                full_name=payload.get("user_metadata", {}).get("full_name"),
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### 6. Backend: User Sync Endpoint

#### 文件: `app/api/v1/endpoints/auth.py`
```python
@router.post("/sync-user", response_model=UserResponse)
async def sync_user_with_supabase(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    同步 Supabase 用户到本地数据库

    前端在登录后调用此接口，确保用户数据同步
    """
    return UserResponse.from_orm(current_user)
```

### 7. Database: User Model Update

#### 文件: `app/models/user.py`
```python
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    supabase_user_id = Column(String, unique=True, index=True, nullable=False)  # 新增
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)  # 新增：从 OAuth 获取

    # 移除密码相关字段
    # hashed_password = Column(String, nullable=False)  # 删除

    # 积分系统
    credits = Column(Integer, default=10)

    # 状态
    is_active = Column(Boolean, default=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### 8. Database Migration

#### 迁移脚本: `alembic/versions/xxx_add_supabase_user_id.py`
```python
"""add supabase_user_id to users

Revision ID: xxx
Revises: yyy
Create Date: 2025-xx-xx

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # 添加 supabase_user_id 列
    op.add_column('users', sa.Column('supabase_user_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_supabase_user_id'), 'users', ['supabase_user_id'], unique=True)

    # 添加 avatar_url 列
    op.add_column('users', sa.Column('avatar_url', sa.String(), nullable=True))

    # 删除 hashed_password 列（慎重！）
    # op.drop_column('users', 'hashed_password')

def downgrade():
    op.drop_index(op.f('ix_users_supabase_user_id'), table_name='users')
    op.drop_column('users', 'supabase_user_id')
    op.drop_column('users', 'avatar_url')
    # op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
```

## Data Flow

### User Login Flow (Email + Password)

```
1. 用户在前端输入邮箱和密码
2. 调用 supabase.auth.signInWithPassword({email, password})
3. Supabase 验证凭据，返回 JWT access_token
4. 前端存储 JWT 到 localStorage
5. 前端调用后端 /api/v1/auth/sync-user，携带 JWT
6. 后端验证 JWT，从 Supabase 获取用户信息
7. 后端同步用户数据到本地数据库
8. 返回用户信息给前端
```

### User Login Flow (OAuth - Google/GitHub)

```
1. 用户点击 "使用 Google 登录" 按钮
2. 调用 supabase.auth.signInWithOAuth({ provider: 'google' })
3. 重定向到 Google OAuth 授权页面
4. 用户授权后，Google 重定向回应用 (callback URL)
5. Supabase 验证 OAuth 响应，创建/更新用户
6. Supabase 签发 JWT access_token
7. 前端检测 session 变化 (onAuthStateChange)
8. 前端调用后端 /api/v1/auth/sync-user，携带 JWT
9. 后端验证 JWT，同步用户数据
10. 返回用户信息给前端
```

### API Request Flow (Authenticated)

```
1. 前端发起 API 请求 (例如: POST /api/v1/generations/)
2. 从 localStorage 获取 Supabase JWT
3. 添加 Authorization: Bearer <JWT> header
4. 后端 get_current_user dependency 验证 JWT
5. 从 JWT 中提取 supabase_user_id
6. 查询本地数据库获取完整用户信息
7. 继续处理请求
```

## Security Considerations

### 1. JWT Verification
- **问题**: 如何验证 Supabase 签发的 JWT？
- **方案**: 使用 Supabase 公钥 (JWKS) 验证 JWT 签名
- **实现**: 定期从 Supabase JWKS endpoint 获取公钥并缓存

### 2. User Data Sync
- **问题**: 如何确保 Supabase 用户和本地用户数据同步？
- **方案**:
  - 首次登录时自动创建本地用户
  - 使用 `supabase_user_id` 作为唯一标识
  - 定期同步用户元数据 (可选)

### 3. Token Storage
- **问题**: JWT 存储在哪里？
- **方案**:
  - 前端: localStorage (Supabase SDK 默认)
  - 后端: 不存储，每次请求验证
- **风险**: XSS 攻击可能窃取 token
- **缓解**: 实施 CSP 策略，设置 HttpOnly cookies (可选)

### 4. OAuth Callback Security
- **问题**: OAuth 回调 URL 可能被劫持
- **方案**:
  - 使用 HTTPS
  - 验证 state parameter
  - Supabase 自动处理 PKCE flow

### 5. API Key Protection
- **问题**: Supabase API keys 需要保密
- **方案**:
  - 前端只使用 `anon` key (公开可见，但受 RLS 保护)
  - 后端使用 `service_role` key (绝对保密)
  - 使用环境变量管理

## Configuration

### Environment Variables

#### Frontend (.env)
```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
VITE_API_BASE_URL=http://localhost:8000
```

#### Backend (.env)
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # 保密！
SUPABASE_JWT_SECRET=your-jwt-secret  # 用于验证 JWT 签名
```

### Supabase Project Setup

1. **创建项目**: 在 Supabase Dashboard 创建新项目
2. **配置 OAuth Providers**:
   - Google: 添加 Client ID 和 Client Secret
   - GitHub: 添加 OAuth App credentials
3. **设置 Redirect URLs**:
   - Development: `http://localhost:5173/auth/callback`
   - Production: `https://yourapp.com/auth/callback`
4. **配置 Email Templates** (可选)
5. **禁用 RLS** (Row Level Security) 或配置策略

## Testing Strategy

### Unit Tests
- 前端: 测试 AuthContext 各种登录方法
- 后端: 测试 JWT 验证逻辑
- 后端: 测试用户同步逻辑

### Integration Tests
- 测试完整的登录流程 (邮箱+密码)
- 测试 OAuth 回调处理
- 测试 API 请求携带 JWT

### E2E Tests
- 测试用户注册流程
- 测试 Google OAuth 登录 (使用 test accounts)
- 测试登出和 session 清理

## Rollout Plan

### Stage 1: Development (Week 1)
- 创建 Supabase 项目
- 前端集成 Supabase SDK
- 后端实现 JWT 验证

### Stage 2: Feature Branch Testing (Week 2)
- 完成所有代码变更
- 单元测试和集成测试
- Code review

### Stage 3: Staging Deployment (Week 2-3)
- 部署到 staging 环境
- 手动测试所有登录方式
- 性能测试

### Stage 4: Production Rollout (Week 3)
- 部署到生产环境
- 监控错误日志
- 准备回滚方案

### Stage 5: Cleanup (Week 4)
- 移除旧的认证代码
- 更新文档
- 用户迁移 (如需要)

## Performance Considerations

### JWT Verification Caching
- 缓存 Supabase JWKS 减少网络请求
- 使用 `lru_cache` 或 Redis

### User Data Sync
- 首次登录时同步，后续请求不重复同步
- 使用 database indexing 加速查询

### OAuth Redirect Speed
- 优化回调页面加载速度
- 使用 loading 状态提升体验

## Monitoring and Observability

### Metrics to Track
- 登录成功率 (邮箱、Google、GitHub)
- JWT 验证失败率
- 用户同步延迟
- OAuth 回调成功率

### Logging
- 记录所有认证事件
- 记录 JWT 验证失败原因
- 记录用户同步错误

### Alerts
- JWT 验证失败率 > 5%
- OAuth 登录失败率 > 10%
- Supabase API 错误率增加

## Future Enhancements

### Short Term (Next 3 months)
- 实现 Magic Link 登录
- 添加用户头像上传
- 实现密码重置流程

### Long Term (6+ months)
- Two-Factor Authentication (2FA)
- 社交账号绑定/解绑
- 角色和权限系统 (RBAC)
- 自定义邮件模板
