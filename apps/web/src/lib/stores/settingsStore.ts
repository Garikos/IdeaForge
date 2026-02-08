import { create } from "zustand";
import type { LlmProviderInfo } from "@/types/settings";

interface SettingsState {
  currentProvider: string;
  providers: LlmProviderInfo[];
  setCurrentProvider: (provider: string) => void;
  setProviders: (providers: LlmProviderInfo[]) => void;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  currentProvider: "groq",
  providers: [],

  setCurrentProvider: (provider) => set({ currentProvider: provider }),
  setProviders: (providers) => set({ providers }),
}));
