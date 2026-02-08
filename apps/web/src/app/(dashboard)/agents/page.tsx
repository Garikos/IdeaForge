"use client";

import { useEffect } from "react";
import { useAgentStore } from "@/lib/stores/agentStore";
import { AgentCard } from "@/components/agents/AgentCard";
import { api } from "@/lib/api";
import { ru } from "@/lib/i18n/ru";
import type { AgentInfo } from "@/types/agent";

const categoryOrder = ["search_trends", "social", "content", "tech", "news", "economy"];

export default function AgentsPage() {
  const { agents, setAgents, toggleAgent } = useAgentStore();

  useEffect(() => {
    api.getAgents().then((data) => setAgents(data as AgentInfo[]));
  }, [setAgents]);

  const groupedAgents = categoryOrder.map((cat) => ({
    category: cat,
    label: ru.categories[cat as keyof typeof ru.categories] || cat,
    items: agents.filter((a) => a.category === cat),
  })).filter((g) => g.items.length > 0);

  return (
    <div className="max-w-4xl">
      <h1 className="text-2xl font-bold mb-2">Агенты-исследователи</h1>
      <p className="text-[var(--muted-foreground)] mb-6">
        15 бесплатных источников данных для анализа рынка
      </p>

      {groupedAgents.map((group) => (
        <div key={group.category} className="mb-8">
          <h2 className="text-lg font-semibold mb-3 text-[var(--primary)]">
            {group.label}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {group.items.map((agent) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                onToggle={() => toggleAgent(agent.id)}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
