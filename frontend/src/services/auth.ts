/**
 * 认证服务 API
 */
import axios from 'axios';
import type { User as SupabaseUser } from '@supabase/supabase-js';
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  User
} from '@/types/auth';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

// 创建不带认证拦截器的 axios 实例（用于登录/注册）
const authApi = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 用户注册
 */
export async function register(data: RegisterRequest): Promise<TokenResponse> {
  const response = await authApi.post<TokenResponse>('/api/v1/auth/register', data);
  return response.data;
}

/**
 * 用户登录
 */
export async function login(data: LoginRequest): Promise<TokenResponse> {
  const response = await authApi.post<TokenResponse>('/api/v1/auth/login', data);
  return response.data;
}

/**
 * 刷新 access token
 */
export async function refreshAccessToken(refreshToken: string): Promise<TokenResponse> {
  const response = await authApi.post<TokenResponse>('/api/v1/auth/refresh', {
    refresh_token: refreshToken
  });
  return response.data;
}

/**
 * 用户登出
 */
export async function logout(accessToken: string): Promise<void> {
  await authApi.post('/api/v1/auth/logout', null, {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });
}

/**
 * 获取当前用户信息
 */
export async function getCurrentUser(accessToken: string) {
  const response = await authApi.get('/api/v1/auth/me', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });
  return response.data;
}

/**
 * 同步 Supabase 用户到后端
 */
export async function syncUser(supabaseUser: SupabaseUser, accessToken: string): Promise<User> {
  const response = await authApi.post<User>(
    '/api/v1/auth/sync-user',
    {
      supabase_user_id: supabaseUser.id,
      email: supabaseUser.email,
      username: supabaseUser.user_metadata?.username || supabaseUser.email?.split('@')[0],
      avatar_url: supabaseUser.user_metadata?.avatar_url || null,
    },
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    }
  );
  return response.data;
}
