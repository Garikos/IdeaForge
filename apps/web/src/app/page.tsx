"use client";

import Link from "next/link";

export default function HomePage() {
  return (
    <div className="max-w-4xl">
      <h1 className="text-3xl font-bold mb-2">IdeaForge</h1>
      <p className="text-[var(--muted-foreground)] mb-8">
        Мульти-агентная платформа для поиска бизнес-идей с помощью AI
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link
          href="/research"
          className="group rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 hover:border-[var(--primary)] transition-colors"
        >
          <h2 className="text-lg font-semibold mb-2 group-hover:text-[var(--primary)]">
            Исследование
          </h2>
          <p className="text-sm text-[var(--muted-foreground)]">
            Запустите AI-агентов для анализа трендов и поиска бизнес-идей
          </p>
        </Link>

        <Link
          href="/agents"
          className="group rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 hover:border-[var(--primary)] transition-colors"
        >
          <h2 className="text-lg font-semibold mb-2 group-hover:text-[var(--primary)]">
            Агенты
          </h2>
          <p className="text-sm text-[var(--muted-foreground)]">
            15 бесплатных агентов: Google, Reddit, YouTube, GitHub и другие
          </p>
        </Link>

        <Link
          href="/settings"
          className="group rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 hover:border-[var(--primary)] transition-colors"
        >
          <h2 className="text-lg font-semibold mb-2 group-hover:text-[var(--primary)]">
            Настройки
          </h2>
          <p className="text-sm text-[var(--muted-foreground)]">
            Выбор LLM провайдера и настройка агентов
          </p>
        </Link>
      </div>
    </div>
  );
}
