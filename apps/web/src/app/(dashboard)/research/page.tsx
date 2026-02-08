"use client";

import { useState, useEffect } from "react";
import { useResearchStore } from "@/lib/stores/researchStore";
import { ResearchForm } from "@/components/research/ResearchForm";
import { AgentActivityFeed } from "@/components/agents/AgentActivityFeed";
import { IdeaCard } from "@/components/research/IdeaCard";
import { api } from "@/lib/api";
import { WebSocketClient } from "@/lib/websocket";
import type { ResearchRun, IdeaListResponse } from "@/types/research";

export default function ResearchPage() {
  const {
    currentRun,
    ideas,
    isLoading,
    setCurrentRun,
    setIdeas,
    setLoading,
    updateAgentStatus,
    setError,
  } = useResearchStore();

  const [ws, setWs] = useState<WebSocketClient | null>(null);

  useEffect(() => {
    const client = new WebSocketClient("research");
    client.connect();
    client.on("*", (data) => {
      const d = data as Record<string, string>;
      if (d.type === "agent_started" || d.type === "agent_completed" || d.type === "agent_failed") {
        updateAgentStatus({
          agent_name: d.agent_name,
          status: d.type === "agent_started" ? "running" : d.type === "agent_completed" ? "completed" : "failed",
          duration_seconds: null,
          result_summary: d.type === "agent_completed" ? (d.summary ?? null) : null,
          error_message: d.type === "agent_failed" ? (d.error ?? null) : null,
        });
      }
      if (d.type === "research_completed") {
        loadIdeas();
        setLoading(false);
      }
      if (d.type === "research_failed") {
        setError(d.error ?? "Произошла ошибка");
        setLoading(false);
      }
    });
    setWs(client);
    return () => client.disconnect();
  }, []);

  const loadIdeas = async () => {
    try {
      const data = (await api.getIdeas()) as IdeaListResponse;
      setIdeas(data.items, data.total);
    } catch {
      // Ideas may not be available yet
    }
  };

  const handleStartResearch = async (query: string, sources: string[], llmProvider: string) => {
    setLoading(true);
    setError(null);
    try {
      const run = (await api.startResearch({ query, sources, llm_provider: llmProvider })) as ResearchRun;
      setCurrentRun(run);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка запуска");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl">
      <h1 className="text-2xl font-bold mb-6">Исследование рынка</h1>

      <ResearchForm onSubmit={handleStartResearch} isLoading={isLoading} />

      {currentRun && (
        <div className="mt-8">
          <h2 className="text-lg font-semibold mb-4">Активность агентов</h2>
          <AgentActivityFeed />
        </div>
      )}

      {ideas.length > 0 && (
        <div className="mt-8">
          <h2 className="text-lg font-semibold mb-4">
            Найденные идеи ({ideas.length})
          </h2>
          <div className="space-y-4">
            {ideas.map((idea) => (
              <IdeaCard key={idea.id} idea={idea} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
