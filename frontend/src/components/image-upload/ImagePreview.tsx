/**
 * 图片预览组件
 */
import { X, RotateCcw } from "lucide-react";
import type { UploadedImage } from "@/types/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface ImagePreviewProps {
  image: UploadedImage;
  onClear: () => void;
  onReupload?: () => void;
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

export function ImagePreview({ image, onClear, onReupload }: ImagePreviewProps) {
  const imageUrl = `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}${image.storage_path}`;

  return (
    <Card className="mt-4">
      <CardContent className="p-4">
        <div className="flex gap-4">
          {/* 图片缩略图 */}
          <div className="flex-shrink-0">
            <img
              src={imageUrl}
              alt={image.filename}
              className="w-32 h-32 object-cover rounded-md"
            />
          </div>

          {/* 图片信息 */}
          <div className="flex-1 min-w-0">
            <h3 className="font-medium truncate">{image.filename}</h3>
            <div className="mt-2 space-y-1 text-sm text-muted-foreground">
              <p>大小: {formatFileSize(image.file_size)}</p>
              <p>尺寸: {image.width} × {image.height} px</p>
            </div>

            {/* 操作按钮 */}
            <div className="mt-3 flex gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={onClear}
              >
                <X className="h-4 w-4 mr-1" />
                清除
              </Button>
              {onReupload && (
                <Button
                  size="sm"
                  variant="outline"
                  onClick={onReupload}
                >
                  <RotateCcw className="h-4 w-4 mr-1" />
                  重新上传
                </Button>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
