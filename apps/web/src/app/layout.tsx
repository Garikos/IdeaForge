import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";
import { Sidebar } from "@/components/ui/Sidebar";

export const metadata: Metadata = {
  title: "IdeaForge — Поиск бизнес-идей",
  description: "Мульти-агентная платформа для поиска бизнес-идей с помощью AI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
        <Providers>
          <div className="flex min-h-screen">
            <Sidebar />
            <main className="flex-1 p-6 lg:p-8 ml-64">{children}</main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
