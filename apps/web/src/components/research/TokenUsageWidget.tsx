"use client";

import { useResearchStore } from "@/lib/stores/researchStore";
import { cn } from "@/lib/utils";

function formatNumber(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return String(n);
}

type RateStatus = "ok" | "approaching" | "exceeded";

function getRateStatus(used: number, limit: number | null): RateStatus {
  if (!limit) return "ok";
  const ratio = used / limit;
  if (ratio >= 1) return "exceeded";
  if (ratio >= 0.7) return "approaching";
  return "ok";
}

const statusConfig: Record<RateStatus, { color: string; bg: string; label: string }> = {
  ok: { color: "text-green-600", bg: "bg-green-500", label: "В норме" },
  approaching: { color: "text-yellow-600", bg: "bg-yellow-500", label: "Приближается к лимиту" },
  exceeded: { color: "text-red-600", bg: "bg-red-500", label: "Лимит превышен" },
};

export function TokenUsageWidget() {
  const { tokenUsage, isLoading } = useResearchStore();

  if (!tokenUsage && !isLoading) return null;

  const total = tokenUsage?.total_tokens ?? 0;
  const limit = tokenUsage?.tpm_limit ?? null;
  const calls = tokenUsage?.llm_calls ?? 0;
  const provider = tokenUsage?.provider ?? "";
  const status = getRateStatus(total, limit);
  const config = statusConfig[status];
  const percentage = limit ? Math.min((total / limit) * 100, 100) : 0;

  if (!tokenUsage) return null;

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] px-4 py-3">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-medium text-[var(--muted-foreground)]">
          Использование токенов
        </span>
        <div className="flex items-center gap-1.5">
          <span className={cn("w-2 h-2 rounded-full", config.bg)} />
          <span className={cn("text-xs font-medium", config.color)}>
            {config.label}
          </span>
        </div>
      </div>

      {limit && (
        <div className="w-full h-1.5 bg-[var(--muted)] rounded-full mb-2">
          <div
            className={cn(
              "h-full rounded-full transition-all duration-300",
              status === "exceeded" ? "bg-red-500" :
              status === "approaching" ? "bg-yellow-500" : "bg-green-500"
            )}
            style={{ width: `${percentage}%` }}
          />
        </div>
      )}

      <div className="flex items-center justify-between text-xs text-[var(--muted-foreground)]">
        <span className="tabular-nums">
          {formatNumber(total)} {limit ? `/ ${formatNumber(limit)} TPM` : "токенов"}
        </span>
        <span className="tabular-nums">
          {calls} {calls === 1 ? "вызов" : "вызовов"} LLM
        </span>
      </div>

      {provider && (
        <div className="mt-1 text-xs text-[var(--muted-foreground)] opacity-70">
          {provider}
        </div>
      )}
    </div>
  );
}
