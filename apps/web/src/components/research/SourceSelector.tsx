"use client";

import { cn } from "@/lib/utils";

const SOURCE_GROUPS = [
  {
    label: "Поисковые тренды",
    sources: [
      { id: "google_trends", name: "Google Trends" },
      { id: "google_search", name: "Google Search" },
      { id: "wikipedia", name: "Wikipedia" },
    ],
  },
  {
    label: "Социальные",
    sources: [
      { id: "reddit", name: "Reddit" },
      { id: "hackernews", name: "Hacker News" },
      { id: "devto", name: "DEV.to" },
      { id: "bluesky", name: "Bluesky" },
    ],
  },
  {
    label: "Контент",
    sources: [{ id: "youtube", name: "YouTube" }],
  },
  {
    label: "Технологии",
    sources: [
      { id: "github", name: "GitHub" },
      { id: "packages", name: "npm/PyPI" },
    ],
  },
  {
    label: "Новости",
    sources: [{ id: "news", name: "GNews" }],
  },
  {
    label: "Экономика",
    sources: [{ id: "economic", name: "BLS/World Bank" }],
  },
];

interface Props {
  selected: string[];
  onChange: (sources: string[]) => void;
}

export function SourceSelector({ selected, onChange }: Props) {
  const toggle = (id: string) => {
    onChange(
      selected.includes(id)
        ? selected.filter((s) => s !== id)
        : [...selected, id]
    );
  };

  return (
    <div className="space-y-3">
      {SOURCE_GROUPS.map((group) => (
        <div key={group.label}>
          <span className="text-xs text-[var(--muted-foreground)] font-medium">
            {group.label}
          </span>
          <div className="flex flex-wrap gap-2 mt-1">
            {group.sources.map((src) => (
              <button
                key={src.id}
                type="button"
                onClick={() => toggle(src.id)}
                className={cn(
                  "text-xs px-3 py-1.5 rounded-full border transition-colors",
                  selected.includes(src.id)
                    ? "border-[var(--primary)] bg-[var(--primary)] text-[var(--primary-foreground)]"
                    : "border-[var(--border)] text-[var(--muted-foreground)] hover:border-[var(--primary)]"
                )}
              >
                {src.name}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
