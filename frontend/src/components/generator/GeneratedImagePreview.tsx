/**
 * 生成结果图片预览组件
 */
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, RotateCcw, X } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { useState } from "react";

interface GeneratedImagePreviewProps {
  imageUrl: string;
  onRegenerate: () => void;
  onClear: () => void;
}

export function GeneratedImagePreview({
  imageUrl,
  onRegenerate,
  onClear,
}: GeneratedImagePreviewProps) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const fullImageUrl = `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}${imageUrl}`;

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = fullImageUrl;
    link.download = `petsphoto_${Date.now()}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Card className="mt-4 max-w-xs">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-green-600">✓ 生成完成</h3>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClear}
            className="h-6 w-6"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        <div className="relative">
          {!imageLoaded && <Skeleton className="w-full aspect-square rounded-lg" />}
          <img
            src={fullImageUrl}
            alt="Generated avatar"
            className={`w-full rounded-lg ${imageLoaded ? "" : "hidden"}`}
            onLoad={() => setImageLoaded(true)}
            onError={() => setImageLoaded(true)}
          />
        </div>

        <div className="grid grid-cols-2 gap-2 mt-4">
          <Button variant="outline" onClick={onRegenerate} className="w-full">
            <RotateCcw className="h-4 w-4 mr-2" />
            重新生成
          </Button>
          <Button onClick={handleDownload} className="w-full">
            <Download className="h-4 w-4 mr-2" />
            下载图片
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
