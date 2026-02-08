"use client";

import { useEffect } from "react";
import { useSettingsStore } from "@/lib/stores/settingsStore";
import { LlmSelector } from "@/components/settings/LlmSelector";
import { AgentToggle } from "@/components/settings/AgentToggle";
import { api } from "@/lib/api";
import type { LlmSettings } from "@/types/settings";

export default function SettingsPage() {
  const { setCurrentProvider, setProviders } = useSettingsStore();

  useEffect(() => {
    api.getLlmSettings().then((data) => {
      const settings = data as LlmSettings;
      setCurrentProvider(settings.current_provider);
      setProviders(settings.providers);
    });
  }, [setCurrentProvider, setProviders]);

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-6">Настройки</h1>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-2">LLM Провайдер</h2>
        <p className="text-sm text-[var(--muted-foreground)] mb-4">
          Выберите модель для работы агентов. Groq рекомендуется (бесплатно и быстро).
        </p>
        <LlmSelector />
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-2">Агенты-исследователи</h2>
        <p className="text-sm text-[var(--muted-foreground)] mb-4">
          Включите или выключите источники данных для исследований.
        </p>
        <AgentToggle />
      </section>
    </div>
  );
}
