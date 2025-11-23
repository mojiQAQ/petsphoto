/**
 * 生成历史组件
 */
import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { getUserHistory } from '@/services/history';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { Download, RotateCcw } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import type { HistoryItem } from '@/types/history';

interface GenerationHistoryProps {
  onRegenerate?: (styleId: string) => void;
}

export function GenerationHistory({ onRegenerate }: GenerationHistoryProps) {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  const [selectedItem, setSelectedItem] = useState<HistoryItem | null>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ['history'],
    queryFn: () => getUserHistory(20, 0),
  });

  // 下载图片
  const handleDownload = async () => {
    if (!selectedItem?.result_image_url) return;

    try {
      const imageUrl = `${apiBaseUrl}${selectedItem.result_image_url}`;
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `petsphoto_${Date.now()}.jpg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('下载失败:', error);
    }
  };

  // 重新生成
  const handleRegenerate = () => {
    if (selectedItem && onRegenerate) {
      onRegenerate(selectedItem.style_id);
      setSelectedItem(null);
    }
  };

  if (isLoading) {
    return (
      <div>
        <h2 className="text-2xl font-bold mb-6">生成历史</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => (
            <Card key={i} className="p-0 overflow-hidden">
              <Skeleton className="w-full aspect-square" />
              <div className="p-3 space-y-2">
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-3 w-1/2" />
              </div>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h2 className="text-2xl font-bold mb-6">生成历史</h2>
        <Alert variant="destructive">
          加载历史记录失败:{' '}
          {error instanceof Error ? error.message : '未知错误'}
        </Alert>
      </div>
    );
  }

  if (!data || data.items.length === 0) {
    return (
      <div>
        <h2 className="text-2xl font-bold mb-6">生成历史</h2>
        <Card className="p-12 text-center">
          <p className="text-muted-foreground">还没有生成记录</p>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">生成历史</h2>
        <p className="text-sm text-muted-foreground">共 {data.total} 条记录</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {data.items.map((item) => (
          <Card
            key={item.id}
            className="p-0 overflow-hidden group cursor-pointer hover:shadow-md transition-shadow"
            onClick={() => {
              if (item.result_image_url && item.status === 'completed') {
                setSelectedItem(item);
              }
            }}
          >
            {/* Image */}
            <div className="relative aspect-square bg-muted">
              {item.result_image_url && item.status === 'completed' ? (
                <img
                  src={`${apiBaseUrl}${item.result_image_url}`}
                  alt="Generated result"
                  className="w-full h-full object-cover"
                  loading="lazy"
                  onError={(e) => {
                    console.error('Image load error:', item.result_image_url);
                    e.currentTarget.style.display = 'none';
                  }}
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-sm text-muted-foreground">
                  {item.status === 'pending' && '等待中'}
                  {item.status === 'processing' && '生成中...'}
                  {item.status === 'failed' && '生成失败'}
                </div>
              )}
            </div>

            {/* Info */}
            <div className="p-3 space-y-1">
              <p className="text-xs text-muted-foreground line-clamp-1">
                风格: {item.style_id}
              </p>
              <p className="text-xs text-muted-foreground">
                {formatDistanceToNow(new Date(item.created_at), {
                  addSuffix: true,
                  locale: zhCN,
                })}
              </p>
            </div>
          </Card>
        ))}
      </div>

      {/* 图片预览对话框 */}
      <Dialog open={!!selectedItem} onOpenChange={() => setSelectedItem(null)}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>历史记录</DialogTitle>
          </DialogHeader>
          {selectedItem?.result_image_url && (
            <div className="flex justify-center">
              <img
                src={`${apiBaseUrl}${selectedItem.result_image_url}`}
                alt="历史记录预览"
                className="max-w-full h-auto rounded-lg"
              />
            </div>
          )}
          <DialogFooter className="gap-2">
            {onRegenerate && (
              <Button variant="outline" onClick={handleRegenerate}>
                <RotateCcw className="h-4 w-4 mr-2" />
                重新生成
              </Button>
            )}
            <Button onClick={handleDownload}>
              <Download className="h-4 w-4 mr-2" />
              下载图片
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
