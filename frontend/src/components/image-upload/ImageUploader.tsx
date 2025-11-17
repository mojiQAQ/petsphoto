/**
 * 图片上传组件
 */
import { useState, useRef, ChangeEvent, DragEvent } from "react";
import { Upload, AlertCircle } from "lucide-react";
import { uploadImage } from "@/services/api";
import type { UploadedImage } from "@/types/api";
import { useToast } from "@/hooks/use-toast";

interface ImageUploaderProps {
  onUploadSuccess: (image: UploadedImage) => void;
  onUploadError?: (error: string) => void;
  maxSizeInMB?: number;
  acceptedFormats?: string[];
}

const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];
const MAX_SIZE_MB = 10;

export function ImageUploader({
  onUploadSuccess,
  onUploadError,
  maxSizeInMB = MAX_SIZE_MB,
  acceptedFormats = ALLOWED_TYPES,
}: ImageUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const validateFile = (file: File): string | null => {
    // 验证文件类型
    if (!acceptedFormats.includes(file.type)) {
      return "仅支持 JPG、PNG 和 WEBP 格式";
    }

    // 验证文件大小
    const maxSizeBytes = maxSizeInMB * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      return `图片大小不能超过 ${maxSizeInMB}MB`;
    }

    if (file.size < 1024) {
      return "文件大小过小，可能已损坏";
    }

    return null;
  };

  const handleFile = async (file: File) => {
    // 验证文件
    const error = validateFile(file);
    if (error) {
      toast({
        variant: "destructive",
        title: "上传失败",
        description: error,
      });
      onUploadError?.(error);
      return;
    }

    setIsUploading(true);

    try {
      const uploadedImage = await uploadImage(file);
      onUploadSuccess(uploadedImage);
      toast({
        title: "上传成功",
        description: "图片已成功上传",
      });
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || "上传失败，请重试";
      toast({
        variant: "destructive",
        title: "上传失败",
        description: errorMsg,
      });
      onUploadError?.(errorMsg);
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div
      onClick={handleClick}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      className={`
        relative flex flex-col items-center justify-center
        border-2 border-dashed rounded-lg p-8
        cursor-pointer transition-colors
        ${isDragging ? "border-primary bg-primary/5" : "border-gray-300 hover:border-primary/50"}
        ${isUploading ? "opacity-50 cursor-not-allowed" : ""}
      `}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept={acceptedFormats.join(",")}
        onChange={handleFileChange}
        className="hidden"
        disabled={isUploading}
      />

      <div className="flex flex-col items-center gap-4">
        {isUploading ? (
          <>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            <p className="text-sm text-muted-foreground">上传中...</p>
          </>
        ) : (
          <>
            <Upload className="h-12 w-12 text-muted-foreground" />
            <div className="text-center">
              <p className="text-sm font-medium">拖拽图片到这里，或点击上传</p>
              <p className="text-xs text-muted-foreground mt-2">
                支持 JPG、PNG、WEBP 格式，最大 {maxSizeInMB}MB
              </p>
            </div>
          </>
        )}
      </div>

      {isDragging && (
        <div className="absolute inset-0 bg-primary/10 rounded-lg pointer-events-none" />
      )}
    </div>
  );
}
