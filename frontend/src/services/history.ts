/**
 * 历史记录服务 API
 */
import axios from 'axios';
import type { HistoryResponse } from '@/types/history';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

// 创建带认证拦截器的 axios 实例
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器：自动添加 Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('petsphoto_access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * 获取用户的生成历史
 */
export async function getUserHistory(
  limit: number = 20,
  offset: number = 0
): Promise<HistoryResponse> {
  const response = await api.get<HistoryResponse>(
    `/api/v1/users/me/history?limit=${limit}&offset=${offset}`
  );
  return response.data;
}
