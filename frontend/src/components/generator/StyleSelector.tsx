/**
 * 风格选择器组件
 */
import { useQuery } from "@tanstack/react-query";
import { fetchStyles } from "@/services/api";
import type { GenerationStyle } from "@/types/api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { StyleCard } from "./StyleCard";

interface StyleSelectorProps {
  selectedStyleId: string | null;
  onStyleSelect: (styleId: string) => void;
}

export function StyleSelector({ selectedStyleId, onStyleSelect }: StyleSelectorProps) {
  const {
    data: styles,
    isLoading,
    error,
    refetch,
  } = useQuery<GenerationStyle[]>({
    queryKey: ["styles"],
    queryFn: fetchStyles,
  });

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {[...Array(4)].map((_, i) => (
          <Skeleton key={i} className="h-32" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription className="flex items-center justify-between">
          <span>无法加载风格列表</span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
          >
            重试
          </Button>
        </AlertDescription>
      </Alert>
    );
  }

  if (!styles || styles.length === 0) {
    return (
      <Alert>
        <AlertDescription>暂无可用风格</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {styles.map((style) => (
        <StyleCard
          key={style.id}
          style={style}
          isSelected={selectedStyleId === style.id}
          onClick={() => onStyleSelect(style.id)}
        />
      ))}
    </div>
  );
}
