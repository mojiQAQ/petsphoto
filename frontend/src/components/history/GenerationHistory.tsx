/**
 * 生成历史组件
 */
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getUserHistory } from '@/services/history';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert } from '@/components/ui/alert';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import {
  Dialog,
  DialogContent,
} from '@/components/ui/dialog';

export function GenerationHistory() {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ['history'],
    queryFn: () => getUserHistory(20, 0),
  });

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
                setSelectedImage(`${apiBaseUrl}${item.result_image_url}`);
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
      <Dialog open={!!selectedImage} onOpenChange={() => setSelectedImage(null)}>
        <DialogContent className="max-w-4xl">
          {selectedImage && (
            <img
              src={selectedImage}
              alt="历史记录预览"
              className="w-full h-auto rounded-lg"
            />
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
