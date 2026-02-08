import { create } from "zustand";
import type { AgentInfo } from "@/types/agent";

interface AgentState {
  agents: AgentInfo[];
  setAgents: (agents: AgentInfo[]) => void;
  toggleAgent: (id: string) => void;
}

export const useAgentStore = create<AgentState>((set) => ({
  agents: [],

  setAgents: (agents) => set({ agents }),

  toggleAgent: (id) =>
    set((state) => ({
      agents: state.agents.map((a) =>
        a.id === id ? { ...a, enabled: !a.enabled } : a
      ),
    })),
}));
