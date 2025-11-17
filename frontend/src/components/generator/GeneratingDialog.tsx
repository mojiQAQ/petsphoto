/**
 * 生成中对话框组件
 */
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Loader2 } from "lucide-react";

interface GeneratingDialogProps {
  isOpen: boolean;
}

export function GeneratingDialog({ isOpen }: GeneratingDialogProps) {
  return (
    <Dialog open={isOpen}>
      <DialogContent className="sm:max-w-md" onInteractOutside={(e) => e.preventDefault()}>
        <DialogHeader>
          <DialogTitle>正在生成...</DialogTitle>
          <DialogDescription>
            AI 正在为您的宠物创作艺术头像，请稍候
          </DialogDescription>
        </DialogHeader>

        <div className="flex flex-col items-center justify-center py-8">
          <Loader2 className="h-16 w-16 animate-spin text-primary" />
          <p className="mt-4 text-sm text-muted-foreground">
            这可能需要 10-30 秒...
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
