"use client";

import { useEffect, useState } from "react";
import { useResearchStore } from "@/lib/stores/researchStore";
import { cn } from "@/lib/utils";
import { ru } from "@/lib/i18n/ru";

const statusColors: Record<string, string> = {
  pending: "bg-[var(--muted)] text-[var(--muted-foreground)]",
  running: "bg-blue-600 text-white",
  completed: "bg-green-600 text-white",
  failed: "bg-red-600 text-white",
};

const statusIcons: Record<string, string> = {
  pending: "\u23F3",
  running: "\u26A1",
  completed: "\u2705",
  failed: "\u274C",
};

function ElapsedTimer({ startTime }: { startTime: number }) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setElapsed(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);
    return () => clearInterval(interval);
  }, [startTime]);

  const mins = Math.floor(elapsed / 60);
  const secs = elapsed % 60;
  return (
    <span className="text-xs text-[var(--muted-foreground)] tabular-nums">
      {mins > 0 ? `${mins}m ${secs}s` : `${secs}s`}
    </span>
  );
}

interface AgentActivityFeedProps {
  researchStartTime?: number | null;
  wsConnected?: boolean;
  error?: string | null;
}

export function AgentActivityFeed({ researchStartTime, wsConnected, error }: AgentActivityFeedProps) {
  const { agentStatuses, isLoading } = useResearchStore();

  return (
    <div className="space-y-3">
      {/* Connection + timer header */}
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center gap-2">
          <span className={cn(
            "w-2 h-2 rounded-full",
            wsConnected ? "bg-green-500" : "bg-red-500"
          )} />
          <span className="text-[var(--muted-foreground)]">
            {wsConnected ? "WebSocket подключён" : "Переподключение..."}
          </span>
        </div>
        {researchStartTime && isLoading && (
          <ElapsedTimer startTime={researchStartTime} />
        )}
      </div>

      {/* Error display */}
      {error && (
        <div className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-800">
          <span className="font-medium">Ошибка: </span>{error}
        </div>
      )}

      {/* Agent list */}
      {agentStatuses.length === 0 && isLoading && !error && (
        <div className="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-[var(--card)] px-4 py-3">
          <span className="inline-block w-3 h-3 rounded-full bg-blue-500 animate-pulse" />
          <span className="text-sm text-[var(--muted-foreground)]">
            Запуск агентов...
          </span>
        </div>
      )}

      {agentStatuses.map((status) => (
        <div
          key={status.agent_name}
          className="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-[var(--card)] px-4 py-3"
        >
          {/* Status indicator */}
          {status.status === "running" ? (
            <span className="inline-block w-3 h-3 rounded-full bg-blue-500 animate-pulse" />
          ) : (
            <span className="text-sm">{statusIcons[status.status] || statusIcons.pending}</span>
          )}

          {/* Agent name */}
          <span className="text-sm font-medium min-w-[120px]">{status.agent_name}</span>

          {/* Status badge */}
          <span
            className={cn(
              "text-xs px-2 py-0.5 rounded-full font-medium",
              statusColors[status.status] || statusColors.pending
            )}
          >
            {ru.agents.status[status.status as keyof typeof ru.agents.status] || status.status}
          </span>

          {/* Summary or error */}
          {status.result_summary && (
            <span className="text-xs text-[var(--muted-foreground)] truncate flex-1">
              {status.result_summary}
            </span>
          )}
          {status.error_message && (
            <span className="text-xs text-red-600 truncate flex-1">
              {status.error_message}
            </span>
          )}

          {/* Duration */}
          {status.duration_seconds != null && (
            <span className="text-xs text-[var(--muted-foreground)] tabular-nums">
              {status.duration_seconds.toFixed(1)}s
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
