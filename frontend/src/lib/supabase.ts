/**
 * Supabase 客户端配置
 */
import { createClient } from '@supabase/supabase-js';

// 从环境变量获取配置
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// 验证环境变量
if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error(
    'Missing Supabase environment variables. Please check your .env file.'
  );
}

/**
 * Supabase 客户端实例
 * - persistSession: 在 localStorage 中持久化 session
 * - autoRefreshToken: 自动刷新 token
 * - detectSessionInUrl: 检测 URL 中的 session（用于 OAuth 回调）
 */
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    storage: window.localStorage,
  },
});

/**
 * Database types (可以通过 Supabase CLI 生成)
 * 目前使用基本类型，后续可以通过 `npx supabase gen types typescript` 生成
 */
export type Database = {
  public: {
    Tables: {
      // 未来可以添加表定义
    };
  };
};
