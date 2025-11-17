/**
 * 认证状态管理 Context
 */
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { jwtDecode } from 'jwt-decode';
import type { User, LoginRequest, RegisterRequest } from '@/types/auth';
import * as authService from '@/services/auth';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_STORAGE_KEY = 'petsphoto_access_token';
const REFRESH_TOKEN_STORAGE_KEY = 'petsphoto_refresh_token';

/**
 * 检查 token 是否即将过期（5分钟内）
 */
function isTokenExpiringSoon(token: string): boolean {
  try {
    const decoded = jwtDecode<{ exp: number }>(token);
    const expiresAt = decoded.exp * 1000; // 转换为毫秒
    const now = Date.now();
    const fiveMinutes = 5 * 60 * 1000;
    return (expiresAt - now) < fiveMinutes;
  } catch {
    return true;
  }
}

/**
 * 检查 token 是否已过期
 */
function isTokenExpired(token: string): boolean {
  try {
    const decoded = jwtDecode<{ exp: number }>(token);
    return decoded.exp * 1000 < Date.now();
  } catch {
    return true;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * 保存 tokens 到 localStorage
   */
  const saveTokens = useCallback((accessToken: string, refreshToken: string) => {
    localStorage.setItem(TOKEN_STORAGE_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_STORAGE_KEY, refreshToken);
  }, []);

  /**
   * 清除 tokens
   */
  const clearTokens = useCallback(() => {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(REFRESH_TOKEN_STORAGE_KEY);
  }, []);

  /**
   * 获取 access token
   */
  const getAccessToken = useCallback((): string | null => {
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  }, []);

  /**
   * 获取 refresh token
   */
  const getRefreshToken = useCallback((): string | null => {
    return localStorage.getItem(REFRESH_TOKEN_STORAGE_KEY);
  }, []);

  /**
   * 刷新 access token
   */
  const refreshToken = useCallback(async (): Promise<string | null> => {
    const refreshTokenValue = getRefreshToken();
    if (!refreshTokenValue) {
      return null;
    }

    try {
      const response = await authService.refreshAccessToken(refreshTokenValue);
      saveTokens(response.access_token, response.refresh_token);
      setUser(response.user);
      return response.access_token;
    } catch (error) {
      console.error('刷新 token 失败:', error);
      clearTokens();
      setUser(null);
      return null;
    }
  }, [getRefreshToken, saveTokens, clearTokens]);

  /**
   * 加载用户信息
   */
  const loadUser = useCallback(async () => {
    const accessToken = getAccessToken();

    if (!accessToken) {
      setIsLoading(false);
      return;
    }

    // 检查 token 是否过期
    if (isTokenExpired(accessToken)) {
      // 尝试刷新 token
      const newToken = await refreshToken();
      if (!newToken) {
        setIsLoading(false);
        return;
      }
      return;
    }

    // 检查 token 是否即将过期,提前刷新
    if (isTokenExpiringSoon(accessToken)) {
      await refreshToken();
      setIsLoading(false);
      return;
    }

    try {
      const userData = await authService.getCurrentUser(accessToken);
      setUser(userData);
    } catch (error) {
      console.error('获取用户信息失败:', error);
      // 如果获取用户信息失败,尝试刷新 token
      await refreshToken();
    } finally {
      setIsLoading(false);
    }
  }, [getAccessToken, refreshToken]);

  /**
   * 用户登录
   */
  const login = useCallback(async (data: LoginRequest) => {
    const response = await authService.login(data);
    saveTokens(response.access_token, response.refresh_token);
    setUser(response.user);
  }, [saveTokens]);

  /**
   * 用户注册
   */
  const register = useCallback(async (data: RegisterRequest) => {
    const response = await authService.register(data);
    saveTokens(response.access_token, response.refresh_token);
    setUser(response.user);
  }, [saveTokens]);

  /**
   * 用户登出
   */
  const logout = useCallback(async () => {
    const accessToken = getAccessToken();
    if (accessToken) {
      try {
        await authService.logout(accessToken);
      } catch (error) {
        console.error('登出请求失败:', error);
      }
    }
    clearTokens();
    setUser(null);
  }, [getAccessToken, clearTokens]);

  /**
   * 刷新用户信息
   */
  const refreshUser = useCallback(async () => {
    const accessToken = getAccessToken();
    if (!accessToken) return;

    try {
      const userData = await authService.getCurrentUser(accessToken);
      setUser(userData);
    } catch (error) {
      console.error('刷新用户信息失败:', error);
    }
  }, [getAccessToken]);

  // 初始化时加载用户
  useEffect(() => {
    loadUser();
  }, [loadUser]);

  // 设置定时刷新 token（每 10 分钟检查一次）
  useEffect(() => {
    const interval = setInterval(async () => {
      const accessToken = getAccessToken();
      if (accessToken && isTokenExpiringSoon(accessToken)) {
        await refreshToken();
      }
    }, 10 * 60 * 1000); // 10 分钟

    return () => clearInterval(interval);
  }, [getAccessToken, refreshToken]);

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
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
 */
export function getAccessToken(): string | null {
  return localStorage.getItem(TOKEN_STORAGE_KEY);
}
