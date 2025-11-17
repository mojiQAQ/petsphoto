/**
 * 结果展示对话框组件
 */
import { Download, RotateCcw } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useState } from "react";

interface ResultDialogProps {
  imageUrl: string;
  isOpen: boolean;
  onClose: () => void;
  onRegenerate: () => void;
}

export function ResultDialog({ imageUrl, isOpen, onClose, onRegenerate }: ResultDialogProps) {
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

  const handleRegenerate = () => {
    onClose();
    onRegenerate();
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>生成完成！</DialogTitle>
          <DialogDescription>
            您的宠物艺术头像已生成完成
          </DialogDescription>
        </DialogHeader>

        <div className="flex justify-center">
          {!imageLoaded && (
            <Skeleton className="w-full aspect-square" />
          )}
          <img
            src={fullImageUrl}
            alt="Generated avatar"
            className={`max-w-full h-auto rounded-lg ${imageLoaded ? "" : "hidden"}`}
            onLoad={() => setImageLoaded(true)}
            onError={() => setImageLoaded(true)}
          />
        </div>

        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={handleRegenerate}>
            <RotateCcw className="h-4 w-4 mr-2" />
            重新生成
          </Button>
          <Button onClick={handleDownload}>
            <Download className="h-4 w-4 mr-2" />
            下载图片
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
