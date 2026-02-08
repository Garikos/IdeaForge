"use client";

import { useState } from "react";
import { SourceSelector } from "./SourceSelector";
import { cn } from "@/lib/utils";

const PRESETS: Record<string, string[]> = {
  all: [
    "google_trends", "google_search", "wikipedia", "reddit", "hackernews",
    "devto", "bluesky", "youtube", "github", "packages", "news", "economic",
  ],
  tech: ["google_trends", "hackernews", "github", "packages", "devto"],
  business: ["google_trends", "google_search", "reddit", "news", "economic", "youtube"],
  minimal: ["google_trends", "hackernews", "reddit"],
};

interface Props {
  onSubmit: (query: string, sources: string[], llmProvider: string) => void;
  isLoading: boolean;
}

export function ResearchForm({ onSubmit, isLoading }: Props) {
  const [query, setQuery] = useState("");
  const [selectedSources, setSelectedSources] = useState<string[]>(PRESETS.minimal);

  const handlePreset = (key: string) => {
    setSelectedSources(PRESETS[key] || []);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || selectedSources.length === 0) return;
    onSubmit(query.trim(), selectedSources, "groq");
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">
          Запрос для исследования
        </label>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Опишите область для поиска бизнес-идей, например: AI инструменты для малого бизнеса..."
          className="w-full rounded-lg border border-[var(--border)] bg-[var(--background)] p-3 text-sm min-h-[100px] focus:outline-none focus:ring-2 focus:ring-[var(--ring)]"
          disabled={isLoading}
        />
      </div>

      <div>
        <div className="flex items-center justify-between mb-3">
          <label className="text-sm font-medium">Источники данных</label>
          <div className="flex gap-2">
            {[
              { key: "all", label: "Все" },
              { key: "tech", label: "Тех-фокус" },
              { key: "business", label: "Бизнес" },
              { key: "minimal", label: "Минимум" },
            ].map((p) => (
              <button
                key={p.key}
                type="button"
                onClick={() => handlePreset(p.key)}
                className="text-xs px-2 py-1 rounded border border-[var(--border)] hover:bg-[var(--accent)] transition-colors"
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>
        <SourceSelector
          selected={selectedSources}
          onChange={setSelectedSources}
        />
      </div>

      <button
        type="submit"
        disabled={isLoading || !query.trim() || selectedSources.length === 0}
        className={cn(
          "px-6 py-2.5 rounded-lg text-sm font-medium transition-colors",
          isLoading
            ? "bg-[var(--muted)] text-[var(--muted-foreground)] cursor-not-allowed"
            : "bg-[var(--primary)] text-[var(--primary-foreground)] hover:opacity-90"
        )}
      >
        {isLoading ? "Исследование запущено..." : "Начать исследование"}
      </button>
    </form>
  );
}
