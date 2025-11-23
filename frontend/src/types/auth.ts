/**
 * 认证相关类型定义
 */

export interface User {
  id: number;
  email: string;
  username?: string;
  full_name?: string | null;
  avatar_url?: string | null;
  credits: number;
  is_active?: boolean;
  is_verified?: boolean;
  created_at: string;
  last_login_at?: string | null;
  supabase_user_id?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  username?: string;
  full_name?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface AuthError {
  detail: string;
}
