/**
 * 生成历史相关类型定义
 */

export interface HistoryItem {
  id: string;
  style_id: string;
  style_name: string | null;
  custom_prompt: string | null;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  result_image_url: string | null;
  credits_cost: number;
  error_message: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface HistoryResponse {
  items: HistoryItem[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}
