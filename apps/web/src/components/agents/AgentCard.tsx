"use client";

import type { AgentInfo } from "@/types/agent";
import { cn } from "@/lib/utils";

interface Props {
  agent: AgentInfo;
  onToggle: () => void;
}

export function AgentCard({ agent, onToggle }: Props) {
  return (
    <div
      className={cn(
        "rounded-lg border p-4 transition-colors",
        agent.enabled
          ? "border-[var(--primary)] bg-[var(--card)]"
          : "border-[var(--border)] bg-[var(--muted)] opacity-60"
      )}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-medium text-sm">{agent.name}</h3>
        <button
          onClick={onToggle}
          className={cn(
            "relative w-10 h-5 rounded-full transition-colors",
            agent.enabled ? "bg-[var(--primary)]" : "bg-[var(--border)]"
          )}
        >
          <span
            className={cn(
              "absolute top-0.5 left-0.5 w-4 h-4 rounded-full bg-white transition-transform",
              agent.enabled && "translate-x-5"
            )}
          />
        </button>
      </div>
      <p className="text-xs text-[var(--muted-foreground)] mb-2">
        {agent.description}
      </p>
      <div className="flex items-center gap-2 text-xs">
        <span className="px-1.5 py-0.5 rounded bg-[var(--success)] text-white">
          {agent.cost === "free" ? "Бесплатно" : agent.cost}
        </span>
        <span className="text-[var(--muted-foreground)]">{agent.limits}</span>
        {!agent.has_api_key && agent.requires_key && (
          <span className="text-[var(--warning)]">Нет API-ключа</span>
        )}
      </div>
    </div>
  );
}
