"use client";

import { useSettingsStore } from "@/lib/stores/settingsStore";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

export function LlmSelector() {
  const { currentProvider, providers, setCurrentProvider } = useSettingsStore();

  const handleSelect = async (providerId: string) => {
    try {
      await api.updateLlmProvider(providerId);
      setCurrentProvider(providerId);
    } catch {
      // Handle error
    }
  };

  if (providers.length === 0) {
    return <p className="text-sm text-[var(--muted-foreground)]">Загрузка...</p>;
  }

  return (
    <div className="space-y-2">
      {providers.map((p) => (
        <button
          key={p.id}
          onClick={() => handleSelect(p.id)}
          className={cn(
            "w-full text-left rounded-lg border p-4 transition-colors",
            p.id === currentProvider
              ? "border-[var(--primary)] bg-[var(--card)]"
              : "border-[var(--border)] bg-[var(--background)] hover:border-[var(--primary)]"
          )}
        >
          <div className="flex items-center justify-between">
            <span className="font-medium text-sm">{p.description}</span>
            <div className="flex items-center gap-2">
              <span
                className={cn(
                  "text-xs px-2 py-0.5 rounded",
                  p.cost === "free"
                    ? "bg-[var(--success)] text-white"
                    : "bg-[var(--warning)] text-white"
                )}
              >
                {p.cost === "free" ? "Бесплатно" : p.cost}
              </span>
              {!p.has_api_key && (
                <span className="text-xs text-[var(--warning)]">Нет ключа</span>
              )}
            </div>
          </div>
          <p className="text-xs text-[var(--muted-foreground)] mt-1">
            {p.model} &middot; Скорость: {p.speed}
          </p>
        </button>
      ))}
    </div>
  );
}
