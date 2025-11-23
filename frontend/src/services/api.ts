/**
 * API 服务层
 */
import axios from "axios";
import type { UploadedImage, GenerationStyle, GenerationJob } from "@/types/api";
import { supabase } from "@/lib/supabase";

// 使用相对路径，通过 Vite 代理转发到后端
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器：自动添加 Authorization header（使用 Supabase session）
api.interceptors.request.use(
  async (config) => {
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      console.log("🔐 API Interceptor - Token:", token ? "存在" : "不存在");
      console.log("🔐 API Interceptor - URL:", config.url);

      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
        console.log("✅ Authorization header 已添加");
      } else {
        console.log("❌ 没有找到 Supabase session token");
      }
    } catch (error) {
      console.error("❌ 获取 Supabase session 失败:", error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * 上传图片
 */
export async function uploadImage(file: File): Promise<UploadedImage> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<UploadedImage>("/api/v1/images/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

/**
 * 获取图片信息
 */
export async function getImage(imageId: string): Promise<UploadedImage> {
  const response = await api.get<UploadedImage>(`/api/v1/images/${imageId}`);
  return response.data;
}

/**
 * 获取所有风格
 */
export async function fetchStyles(): Promise<GenerationStyle[]> {
  const response = await api.get<GenerationStyle[]>("/api/v1/styles/");
  return response.data;
}

/**
 * 创建生成任务
 */
export async function createGenerationJob(
  sourceImageId: string,
  styleId: string
): Promise<GenerationJob> {
  const response = await api.post<GenerationJob>("/api/v1/generations/", {
    source_image_id: sourceImageId,
    style_id: styleId,
  });
  return response.data;
}

/**
 * 获取生成任务状态
 */
export async function getGenerationJob(jobId: string): Promise<GenerationJob> {
  const response = await api.get<GenerationJob>(`/api/v1/generations/${jobId}`);
  return response.data;
}
