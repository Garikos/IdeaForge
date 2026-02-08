"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", label: "Главная", icon: "🏠" },
  { href: "/research", label: "Исследование", icon: "🔍" },
  { href: "/agents", label: "Агенты", icon: "🤖" },
  { href: "/settings", label: "Настройки", icon: "⚙️" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-full w-64 border-r border-[var(--border)] bg-[var(--card)] p-4 flex flex-col">
      <div className="mb-8 px-2">
        <h1 className="text-xl font-bold text-[var(--primary)]">IdeaForge</h1>
        <p className="text-xs text-[var(--muted-foreground)] mt-1">
          AI-поиск бизнес-идей
        </p>
      </div>

      <nav className="flex-1 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors",
              pathname === item.href
                ? "bg-[var(--primary)] text-[var(--primary-foreground)]"
                : "text-[var(--muted-foreground)] hover:bg-[var(--accent)] hover:text-[var(--accent-foreground)]"
            )}
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="border-t border-[var(--border)] pt-4 mt-4">
        <p className="text-xs text-[var(--muted-foreground)] px-2">
          v0.1.0 — MVP
        </p>
      </div>
    </aside>
  );
}
