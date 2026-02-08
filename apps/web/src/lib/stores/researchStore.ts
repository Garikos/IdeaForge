import { create } from "zustand";
import type { BusinessIdea, ResearchRun, TokenUsageEvent } from "@/types/research";
import type { AgentRunStatus } from "@/types/agent";

interface ResearchState {
  currentRun: ResearchRun | null;
  agentStatuses: AgentRunStatus[];
  ideas: BusinessIdea[];
  totalIdeas: number;
  isLoading: boolean;
  error: string | null;
  tokenUsage: TokenUsageEvent | null;
  setCurrentRun: (run: ResearchRun | null) => void;
  setAgentStatuses: (statuses: AgentRunStatus[]) => void;
  updateAgentStatus: (status: AgentRunStatus) => void;
  setIdeas: (ideas: BusinessIdea[], total: number) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setTokenUsage: (usage: TokenUsageEvent | null) => void;
}

export const useResearchStore = create<ResearchState>((set) => ({
  currentRun: null,
  agentStatuses: [],
  ideas: [],
  totalIdeas: 0,
  isLoading: false,
  error: null,
  tokenUsage: null,

  setCurrentRun: (run) => set({ currentRun: run }),

  setAgentStatuses: (statuses) => set({ agentStatuses: statuses }),

  updateAgentStatus: (status) =>
    set((state) => {
      const existing = state.agentStatuses.findIndex(
        (s) => s.agent_name === status.agent_name
      );
      const updated = [...state.agentStatuses];
      if (existing >= 0) {
        updated[existing] = status;
      } else {
        updated.push(status);
      }
      return { agentStatuses: updated };
    }),

  setIdeas: (ideas, total) => set({ ideas, totalIdeas: total }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  setTokenUsage: (tokenUsage) => set({ tokenUsage }),
}));
