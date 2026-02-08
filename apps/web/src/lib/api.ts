const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

// Research
export const api = {
  startResearch: (data: { query: string; sources: string[]; llm_provider: string }) =>
    fetchApi("/research", { method: "POST", body: JSON.stringify(data) }),

  getIdeas: (skip = 0, limit = 20) =>
    fetchApi(`/ideas?skip=${skip}&limit=${limit}`),

  getIdea: (id: number) => fetchApi(`/ideas/${id}`),

  cancelResearch: (runId: string) =>
    fetchApi(`/research/${runId}/cancel`, { method: "POST" }),

  // Agents
  getAgents: () => fetchApi("/agents"),
  getAgentRuns: (runId: string) => fetchApi(`/agents/runs/${runId}`),

  // Settings
  getLlmSettings: () => fetchApi("/settings/llm"),
  updateLlmProvider: (provider: string) =>
    fetchApi("/settings/llm", {
      method: "PUT",
      body: JSON.stringify({ provider }),
    }),
  getAgentSettings: () => fetchApi("/settings/agents"),
  updateAgentSettings: (agents: Record<string, boolean>) =>
    fetchApi("/settings/agents", {
      method: "PUT",
      body: JSON.stringify({ agents }),
    }),
};
