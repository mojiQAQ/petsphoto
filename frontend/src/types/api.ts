/**
 * API 类型定义
 */

export interface UploadedImage {
  id: string;
  filename: string;
  storage_path: string;
  file_size: number;
  width: number;
  height: number;
  mime_type: string;
  created_at: string;
}

export interface GenerationStyle {
  id: string;
  name: string;
  description?: string;
  prompt_template: string;
  sort_order: number;
}

export type GenerationStatus = "pending" | "processing" | "completed" | "failed";

export interface GenerationJob {
  id: string;
  user_id: string;
  source_image_id: string;
  style_id: string;
  status: GenerationStatus;
  result_image_url?: string;
  error_message?: string;
  credits_cost: number;
  created_at: string;
  completed_at?: string;
}
