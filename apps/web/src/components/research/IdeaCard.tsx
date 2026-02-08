"use client";

import type { BusinessIdea } from "@/types/research";

interface Props {
  idea: BusinessIdea;
}

export function IdeaCard({ idea }: Props) {
  const score = idea.composite_score != null ? Math.round(idea.composite_score * 100) : null;

  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <h3 className="font-semibold mb-1">{idea.title}</h3>
          <p className="text-sm text-[var(--muted-foreground)] mb-3">
            {idea.summary}
          </p>
          <div className="flex items-center gap-3 text-xs text-[var(--muted-foreground)]">
            <span className="px-2 py-0.5 rounded bg-[var(--accent)]">
              {idea.source}
            </span>
            <span>{idea.status}</span>
            {idea.source_url && (
              <a
                href={idea.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[var(--primary)] hover:underline"
              >
                Источник
              </a>
            )}
          </div>
        </div>
        {score !== null && (
          <div className="flex flex-col items-center shrink-0">
            <div className="text-2xl font-bold text-[var(--primary)]">
              {score}
            </div>
            <div className="text-xs text-[var(--muted-foreground)]">балл</div>
          </div>
        )}
      </div>
    </div>
  );
}
