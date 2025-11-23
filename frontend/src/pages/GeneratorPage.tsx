/**
 * 生成器页面
 */
import { useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Container } from "@/components/layout/Container";
import { ImageUploader } from "@/components/image-upload/ImageUploader";
import { ImagePreview } from "@/components/image-upload/ImagePreview";
import { StyleSelector } from "@/components/generator/StyleSelector";
import { ResultDialog } from "@/components/generator/ResultDialog";
import { GeneratingDialog } from "@/components/generator/GeneratingDialog";
import { GeneratedImagePreview } from "@/components/generator/GeneratedImagePreview";
import { GenerationHistory } from "@/components/history/GenerationHistory";
import { Button } from "@/components/ui/button";
import { Sparkles } from "lucide-react";
import type { UploadedImage, GenerationJob } from "@/types/api";
import { createGenerationJob } from "@/services/api";
import { useGenerationPolling } from "@/hooks/useGenerationPolling";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/contexts/AuthContext";

export function GeneratorPage() {
  const [uploadedImage, setUploadedImage] = useState<UploadedImage | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string | null>(null);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [completedJob, setCompletedJob] = useState<GenerationJob | null>(null);
  const [isCreatingJob, setIsCreatingJob] = useState(false);
  const [showResultDialog, setShowResultDialog] = useState(false);
  const { toast } = useToast();
  const { isAuthenticated, refreshUser } = useAuth();
  const queryClient = useQueryClient();

  // 轮询生成任务状态
  const { job } = useGenerationPolling({
    jobId: currentJobId,
    onCompleted: async (job) => {
      setCompletedJob(job);
      setShowResultDialog(true);
      setCurrentJobId(null);

      // 刷新历史记录和用户积分
      queryClient.invalidateQueries({ queryKey: ['history'] });
      await refreshUser();

      toast({
        title: "生成完成！",
        description: "您的宠物艺术头像已生成",
      });
    },
    onFailed: (job) => {
      setCurrentJobId(null);
      toast({
        variant: "destructive",
        title: "生成失败",
        description: job.error_message || "请稍后重试",
      });
    },
  });

  const handleGenerate = async () => {
    if (!uploadedImage || !selectedStyle) return;

    // 检查用户是否登录
    if (!isAuthenticated) {
      toast({
        variant: "destructive",
        title: "请先登录",
        description: "生成图片需要登录账号",
      });
      return;
    }

    setIsCreatingJob(true);

    try {
      const job = await createGenerationJob(uploadedImage.id, selectedStyle);
      setCurrentJobId(job.id);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || "创建任务失败，请重试";
      toast({
        variant: "destructive",
        title: "创建失败",
        description: errorMsg,
      });
    } finally {
      setIsCreatingJob(false);
    }
  };

  const handleClearImage = () => {
    setUploadedImage(null);
  };

  const handleRegenerate = () => {
    setCompletedJob(null);
    // 保留当前的图片和风格，用户可以直接再次点击生成
  };

  // 从历史记录重新生成（设置风格并滚动到顶部）
  const handleRegenerateFromHistory = (styleId: string) => {
    setSelectedStyle(styleId);
    // 滚动到页面顶部
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCloseResult = () => {
    // 关闭弹窗但保留 completedJob，这样图片会显示在下方
    setShowResultDialog(false);
  };

  const handleClearGenerated = () => {
    setCompletedJob(null);
  };

  const isGenerating = !!currentJobId || isCreatingJob;
  const canGenerate = uploadedImage && selectedStyle && !isGenerating && isAuthenticated;

  return (
    <Container className="py-8">
      <div className="max-w-6xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl md:text-4xl font-bold mb-2">AI 头像生成器</h1>
          <p className="text-muted-foreground">
            上传宠物照片，选择艺术风格，生成独特头像
          </p>
        </div>

        {/* 主要内容区域 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          {/* 左侧：图片上传和生成结果 */}
          <div>
            <h2 className="text-xl font-semibold mb-4">1. 上传宠物照片</h2>
            {!uploadedImage ? (
              <ImageUploader onUploadSuccess={setUploadedImage} />
            ) : (
              <ImagePreview
                image={uploadedImage}
                onClear={handleClearImage}
                onReupload={handleClearImage}
              />
            )}

            {/* 生成结果展示 */}
            {completedJob?.result_image_url && (
              <GeneratedImagePreview
                imageUrl={completedJob.result_image_url}
                onRegenerate={handleRegenerate}
                onClear={handleClearGenerated}
              />
            )}
          </div>

          {/* 右侧：风格选择 */}
          <div>
            <h2 className="text-xl font-semibold mb-4">2. 选择艺术风格</h2>
            <StyleSelector
              selectedStyleId={selectedStyle}
              onStyleSelect={setSelectedStyle}
            />
          </div>
        </div>

        {/* 生成按钮 */}
        <div className="flex justify-center">
          <Button
            size="lg"
            disabled={!canGenerate}
            onClick={handleGenerate}
            className="px-8"
          >
            {isGenerating ? (
              <>
                <span className="animate-spin mr-2">⏳</span>
                生成中...
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5 mr-2" />
                生成头像
              </>
            )}
          </Button>
        </div>

        {/* 提示文字 */}
        {!isAuthenticated && (
          <p className="text-center text-sm text-destructive mt-4">
            请先登录才能生成图片
          </p>
        )}
        {isAuthenticated && !uploadedImage && (
          <p className="text-center text-sm text-muted-foreground mt-4">
            请先上传图片
          </p>
        )}
        {isAuthenticated && uploadedImage && !selectedStyle && (
          <p className="text-center text-sm text-muted-foreground mt-4">
            请选择一种艺术风格
          </p>
        )}
      </div>

      {/* 生成历史 - 仅在用户登录时显示 */}
      {isAuthenticated && (
        <div className="mt-16 pt-16 border-t">
          <GenerationHistory onRegenerate={handleRegenerateFromHistory} />
        </div>
      )}

      {/* 生成中对话框 */}
      <GeneratingDialog isOpen={isGenerating} />

      {/* 结果展示对话框 */}
      {completedJob?.result_image_url && (
        <ResultDialog
          imageUrl={completedJob.result_image_url}
          isOpen={showResultDialog}
          onClose={handleCloseResult}
          onRegenerate={handleRegenerate}
        />
      )}
    </Container>
  );
}
