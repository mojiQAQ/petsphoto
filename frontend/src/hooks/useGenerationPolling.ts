/**
 * 生成任务轮询 Hook
 */
import { useQuery } from "@tanstack/react-query";
import { useEffect, useRef } from "react";
import { getGenerationJob } from "@/services/api";
import type { GenerationJob } from "@/types/api";

interface UseGenerationPollingOptions {
  jobId: string | null;
  interval?: number;
  onCompleted?: (job: GenerationJob) => void;
  onFailed?: (job: GenerationJob) => void;
}

export function useGenerationPolling({
  jobId,
  interval = 3000,
  onCompleted,
  onFailed,
}: UseGenerationPollingOptions) {
  // 使用 ref 来跟踪回调是否已触发,避免重复调用
  const completedRef = useRef(false);
  const failedRef = useRef(false);

  const { data: job, isLoading } = useQuery({
    queryKey: ["generation-job", jobId],
    queryFn: () => getGenerationJob(jobId!),
    enabled: !!jobId,
    refetchInterval: (data) => {
      if (!data) return interval;

      // 任务完成或失败时停止轮询
      if (data.status === "completed" || data.status === "failed") {
        return false;
      }

      // 继续轮询
      return interval;
    },
    // 90 秒后停止轮询(超时保护)
    refetchIntervalInBackground: false,
    staleTime: 0,
  });

  // 使用 useEffect 来处理状态变化时的回调
  useEffect(() => {
    if (!job) return;

    if (job.status === "completed" && !completedRef.current) {
      completedRef.current = true;
      onCompleted?.(job);
    }

    if (job.status === "failed" && !failedRef.current) {
      failedRef.current = true;
      onFailed?.(job);
    }
  }, [job, onCompleted, onFailed]);

  // 重置 ref 当 jobId 变化时
  useEffect(() => {
    completedRef.current = false;
    failedRef.current = false;
  }, [jobId]);

  return { job, isLoading };
}
