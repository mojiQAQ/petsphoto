/**
 * 认证状态管理 Context - 使用 Supabase Auth
 */
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { supabase } from '@/lib/supabase';
import type { User as SupabaseUser, Session, AuthError } from '@supabase/supabase-js';
import type { User, LoginRequest, RegisterRequest } from '@/types/auth';
import * as authService from '@/services/auth';

interface AuthContextType {
  user: User | null;
  supabaseUser: SupabaseUser | null;
  session: Session | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  signInWithGoogle: () => Promise<void>;
  signInWithGithub: () => Promise<void>;
  getAccessToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [supabaseUser, setSupabaseUser] = useState<SupabaseUser | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * 同步用户数据到后端
   */
  const syncUserWithBackend = useCallback(async (supabaseUser: SupabaseUser, accessToken: string) => {
    try {
      const backendUser = await authService.syncUser(supabaseUser, accessToken);
      setUser(backendUser);
    } catch (error) {
      console.error('同步用户到后端失败:', error);
      // 即使同步失败，仍然保持 Supabase 用户登录状态
      // 创建一个基本的 User 对象
      setUser({
        id: 0, // 临时 ID，后端同步成功后会更新
        email: supabaseUser.email || '',
        username: supabaseUser.email?.split('@')[0] || 'user',
        avatar_url: supabaseUser.user_metadata?.avatar_url || null,
        credits: 0,
        created_at: new Date().toISOString(),
        supabase_user_id: supabaseUser.id,
      });
    }
  }, []);

  /**
   * 处理认证状态变化
   */
  useEffect(() => {
    // 获取初始 session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setSupabaseUser(session?.user ?? null);

      if (session?.user) {
        syncUserWithBackend(session.user, session.access_token);
      }

      setIsLoading(false);
    });

    // 监听认证状态变化
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (_event, session) => {
      setSession(session);
      setSupabaseUser(session?.user ?? null);

      if (session?.user) {
        await syncUserWithBackend(session.user, session.access_token);
      } else {
        setUser(null);
      }
    });

    return () => subscription.unsubscribe();
  }, [syncUserWithBackend]);

  /**
   * 获取 access token
   */
  const getAccessToken = useCallback(async (): Promise<string | null> => {
    const { data, error } = await supabase.auth.getSession();
    if (error || !data.session) {
      return null;
    }
    return data.session.access_token;
  }, []);

  /**
   * 邮箱密码登录
   */
  const login = useCallback(async (data: LoginRequest) => {
    const { data: authData, error } = await supabase.auth.signInWithPassword({
      email: data.email,
      password: data.password,
    });

    if (error) {
      throw new Error(error.message);
    }

    if (authData.user && authData.session) {
      await syncUserWithBackend(authData.user, authData.session.access_token);
    }
  }, [syncUserWithBackend]);

  /**
   * 邮箱密码注册
   */
  const register = useCallback(async (data: RegisterRequest) => {
    const { data: authData, error } = await supabase.auth.signUp({
      email: data.email,
      password: data.password,
      options: {
        data: {
          username: data.username,
        },
      },
    });

    if (error) {
      throw new Error(error.message);
    }

    if (authData.user && authData.session) {
      await syncUserWithBackend(authData.user, authData.session.access_token);
    }
  }, [syncUserWithBackend]);

  /**
   * Google OAuth 登录
   */
  const signInWithGoogle = useCallback(async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });

    if (error) {
      throw new Error(error.message);
    }
  }, []);

  /**
   * GitHub OAuth 登录
   */
  const signInWithGithub = useCallback(async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });

    if (error) {
      throw new Error(error.message);
    }
  }, []);

  /**
   * 登出
   */
  const logout = useCallback(async () => {
    const { error } = await supabase.auth.signOut();
    if (error) {
      console.error('登出失败:', error);
    }
    setUser(null);
    setSupabaseUser(null);
    setSession(null);
  }, []);

  /**
   * 刷新用户信息
   */
  const refreshUser = useCallback(async () => {
    const { data: { session } } = await supabase.auth.getSession();

    if (session?.user) {
      await syncUserWithBackend(session.user, session.access_token);
    }
  }, [syncUserWithBackend]);

  const value: AuthContextType = {
    user,
    supabaseUser,
    session,
    isAuthenticated: !!session,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
    signInWithGoogle,
    signInWithGithub,
    getAccessToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * 使用认证 Context 的 Hook
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth 必须在 AuthProvider 内使用');
  }
  return context;
}

/**
 * 获取 access token 的工具函数
 * @deprecated 使用 useAuth().getAccessToken() 或直接调用 supabase.auth.getSession()
 */
export async function getAccessToken(): Promise<string | null> {
  const { data } = await supabase.auth.getSession();
  return data.session?.access_token ?? null;
}
