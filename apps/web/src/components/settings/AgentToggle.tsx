"use client";

import { useEffect } from "react";
import { useAgentStore } from "@/lib/stores/agentStore";
import { AgentCard } from "@/components/agents/AgentCard";
import { api } from "@/lib/api";
import { ru } from "@/lib/i18n/ru";
import type { AgentInfo } from "@/types/agent";

const categoryOrder = ["search_trends", "social", "content", "tech", "news", "economy"];

export function AgentToggle() {
  const { agents, setAgents, toggleAgent } = useAgentStore();

  useEffect(() => {
    api.getAgents().then((data) => setAgents(data as AgentInfo[]));
  }, [setAgents]);

  const handleToggle = async (id: string) => {
    toggleAgent(id);
    const current = agents.find((a) => a.id === id);
    if (current) {
      await api.updateAgentSettings({ [id]: !current.enabled });
    }
  };

  const grouped = categoryOrder.map((cat) => ({
    category: cat,
    label: ru.categories[cat as keyof typeof ru.categories] || cat,
    items: agents.filter((a) => a.category === cat),
  })).filter((g) => g.items.length > 0);

  return (
    <div className="space-y-6">
      {grouped.map((group) => (
        <div key={group.category}>
          <h3 className="text-sm font-medium mb-2 text-[var(--primary)]">
            {group.label}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {group.items.map((agent) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                onToggle={() => handleToggle(agent.id)}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
