/**
 * 风格卡片组件
 */
import { Check } from "lucide-react";
import type { GenerationStyle } from "@/types/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface StyleCardProps {
  style: GenerationStyle;
  isSelected: boolean;
  onClick: () => void;
}

export function StyleCard({ style, isSelected, onClick }: StyleCardProps) {
  return (
    <Card
      onClick={onClick}
      className={cn(
        "cursor-pointer transition-all hover:shadow-md",
        isSelected && "border-primary border-2 ring-2 ring-primary/20"
      )}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg">{style.name}</CardTitle>
          {isSelected && (
            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary flex items-center justify-center">
              <Check className="h-4 w-4 text-primary-foreground" />
            </div>
          )}
        </div>
        {style.description && (
          <CardDescription>{style.description}</CardDescription>
        )}
      </CardHeader>
      <CardContent>
        <p className="text-xs text-muted-foreground line-clamp-2">
          {style.prompt_template}
        </p>
      </CardContent>
    </Card>
  );
}
