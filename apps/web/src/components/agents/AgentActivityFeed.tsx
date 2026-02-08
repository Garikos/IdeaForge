"use client";

import { useResearchStore } from "@/lib/stores/researchStore";
import { cn } from "@/lib/utils";
import { ru } from "@/lib/i18n/ru";

const statusColors: Record<string, string> = {
  pending: "bg-[var(--muted)] text-[var(--muted-foreground)]",
  running: "bg-[var(--primary)] text-[var(--primary-foreground)]",
  completed: "bg-[var(--success)] text-white",
  failed: "bg-[var(--destructive)] text-white",
};

export function AgentActivityFeed() {
  const { agentStatuses } = useResearchStore();

  if (agentStatuses.length === 0) {
    return (
      <p className="text-sm text-[var(--muted-foreground)]">
        Ожидание запуска агентов...
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {agentStatuses.map((status) => (
        <div
          key={status.agent_name}
          className="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-[var(--card)] px-4 py-3"
        >
          <span
            className={cn(
              "text-xs px-2 py-0.5 rounded-full font-medium",
              statusColors[status.status] || statusColors.pending
            )}
          >
            {ru.agents.status[status.status as keyof typeof ru.agents.status] || status.status}
          </span>
          <span className="text-sm font-medium">{status.agent_name}</span>
          {status.result_summary && (
            <span className="text-xs text-[var(--muted-foreground)] truncate flex-1">
              {status.result_summary}
            </span>
          )}
          {status.error_message && (
            <span className="text-xs text-[var(--destructive)] truncate flex-1">
              {status.error_message}
            </span>
          )}
          {status.duration_seconds != null && (
            <span className="text-xs text-[var(--muted-foreground)]">
              {status.duration_seconds.toFixed(1)}с
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
