"use client";

import { useState, useEffect, useRef } from "react";
import { useResearchStore } from "@/lib/stores/researchStore";
import { ResearchForm } from "@/components/research/ResearchForm";
import { AgentActivityFeed } from "@/components/agents/AgentActivityFeed";
import { TokenUsageWidget } from "@/components/research/TokenUsageWidget";
import { IdeaCard } from "@/components/research/IdeaCard";
import { api } from "@/lib/api";
import { WebSocketClient } from "@/lib/websocket";
import type { ResearchRun, IdeaListResponse, TokenUsageEvent } from "@/types/research";

export default function ResearchPage() {
  const {
    currentRun,
    ideas,
    isLoading,
    error,
    setCurrentRun,
    setIdeas,
    setLoading,
    updateAgentStatus,
    setError,
    setTokenUsage,
  } = useResearchStore();

  const [wsConnected, setWsConnected] = useState(false);
  const [startTime, setStartTime] = useState<number | null>(null);
  const wsRef = useRef<WebSocketClient | null>(null);

  useEffect(() => {
    const client = new WebSocketClient("research");
    wsRef.current = client;

    client.onConnection((connected) => {
      setWsConnected(connected);
    });

    client.on("research_started", () => {
      setStartTime(Date.now());
    });

    client.on("agent_started", (data) => {
      const d = data as Record<string, string>;
      updateAgentStatus({
        agent_name: d.agent_name,
        status: "running",
        duration_seconds: null,
        result_summary: null,
        error_message: null,
      });
    });

    client.on("agent_completed", (data) => {
      const d = data as Record<string, string>;
      updateAgentStatus({
        agent_name: d.agent_name,
        status: "completed",
        duration_seconds: null,
        result_summary: d.summary ?? null,
        error_message: null,
      });
    });

    client.on("agent_failed", (data) => {
      const d = data as Record<string, string>;
      updateAgentStatus({
        agent_name: d.agent_name,
        status: "failed",
        duration_seconds: null,
        result_summary: null,
        error_message: d.error ?? "Ошибка агента",
      });
    });

    client.on("research_completed", () => {
      setLoading(false);
      loadIdeas();
    });

    client.on("research_failed", (data) => {
      const d = data as Record<string, string>;
      setError(d.error ?? "Произошла ошибка исследования");
      setLoading(false);
    });

    client.on("research_cancelled", () => {
      setLoading(false);
      setError(null);
    });

    client.on("token_usage", (data) => {
      setTokenUsage(data as unknown as TokenUsageEvent);
    });

    client.on("research_results", (data) => {
      const d = data as { ideas?: Array<Record<string, unknown>> };
      if (d.ideas && Array.isArray(d.ideas)) {
        setIdeas(d.ideas as never[], d.ideas.length);
        setLoading(false);
      }
    });

    client.connect();

    return () => client.disconnect();
  }, []);

  const loadIdeas = async () => {
    try {
      const data = (await api.getIdeas()) as IdeaListResponse;
      setIdeas(data.items, data.total);
    } catch {
      // Ideas loaded via WS research_results event as fallback
    }
  };

  const handleStartResearch = async (query: string, sources: string[], llmProvider: string) => {
    setLoading(true);
    setError(null);
    setStartTime(Date.now());
    useResearchStore.setState({ agentStatuses: [], ideas: [], tokenUsage: null });

    try {
      const run = (await api.startResearch({ query, sources, llm_provider: llmProvider })) as ResearchRun;
      setCurrentRun(run);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка запуска исследования");
      setLoading(false);
    }
  };

  const handleCancelResearch = async () => {
    const runId = currentRun?.run_id;
    if (!runId) return;
    try {
      await api.cancelResearch(runId);
    } catch {
      // Cancel may fail if already finished
    }
    setLoading(false);
  };

  return (
    <div className="max-w-6xl">
      <h1 className="text-2xl font-bold mb-6">Исследование рынка</h1>

      <ResearchForm
        onSubmit={handleStartResearch}
        onCancel={handleCancelResearch}
        isLoading={isLoading}
      />

      {(currentRun || isLoading || error) && (
        <div className="mt-8">
          <h2 className="text-lg font-semibold mb-4">Активность агентов</h2>
          <AgentActivityFeed
            researchStartTime={startTime}
            wsConnected={wsConnected}
            error={error}
          />
          <div className="mt-3">
            <TokenUsageWidget />
          </div>
        </div>
      )}

      {ideas.length > 0 && (
        <div className="mt-8">
          <h2 className="text-lg font-semibold mb-4">
            Найденные идеи ({ideas.length})
          </h2>
          <div className="space-y-4">
            {ideas.map((idea, i) => (
              <IdeaCard key={idea.id ?? i} idea={idea} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
