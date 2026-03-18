import type { ReactNode } from "react";

import { Badge } from "../ui/badge";


type NavItem = {
  href: string;
  label: string;
};

const navItems: NavItem[] = [
  { href: "#/", label: "总览" },
  { href: "#/repositories", label: "仓库" },
  { href: "#/settings", label: "配置" },
];

type AppShellProps = {
  children?: ReactNode;
  heading?: string;
  kicker?: string;
};

export function AppShell({
  children,
  heading = "GitHub 个人监控台",
  kicker = "Windows Local",
}: AppShellProps) {
  return (
    <div className="min-h-screen">
      <div className="mx-auto max-w-[1440px] px-4 py-6 md:px-8 lg:px-10">
        <header className="grid gap-6 rounded-[36px] border border-line bg-panel p-6 shadow-[var(--shadow)] md:grid-cols-[260px_1fr] md:p-8">
          <div className="space-y-5">
            <div>
              <p className="font-mono text-xs uppercase tracking-[0.35em] text-muted">hit-monittor</p>
              <h1 className="mt-3 font-display text-4xl leading-none md:text-5xl">观察台</h1>
            </div>
            <nav aria-label="主导航">
              <ul className="space-y-2">
                {navItems.map((item, index) => (
                  <li key={item.href}>
                    <a
                      className="flex items-center justify-between rounded-2xl border border-transparent px-4 py-3 text-sm font-semibold text-muted transition hover:border-signal/20 hover:bg-white/80 hover:text-ink"
                      href={item.href}
                    >
                      <span>{item.label}</span>
                      <span className="font-mono text-xs">0{index + 1}</span>
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </div>

          <div className="flex min-h-[260px] flex-col justify-between rounded-[28px] border border-line bg-[linear-gradient(135deg,rgba(255,255,255,0.92),rgba(255,245,235,0.82))] p-6">
            <div className="space-y-4">
              <Badge>{kicker}</Badge>
              <div className="space-y-3">
                <h2 className="max-w-3xl font-display text-4xl leading-tight md:text-6xl">{heading}</h2>
                <p className="max-w-2xl text-sm leading-7 text-muted md:text-base">
                  以编辑台视角展示 GitHub 仓库热点，把 issue、PR、release 压缩成更适合浏览和判断的节奏。
                </p>
              </div>
            </div>
            <div className="mt-6 grid gap-3 text-xs uppercase tracking-[0.22em] text-muted sm:grid-cols-3">
              <div className="rounded-2xl border border-line bg-white/80 px-4 py-3">Issue Focus</div>
              <div className="rounded-2xl border border-line bg-white/80 px-4 py-3">PR Watch</div>
              <div className="rounded-2xl border border-line bg-white/80 px-4 py-3">Release Lens</div>
            </div>
          </div>
        </header>

        <main className="mt-8">{children}</main>
      </div>
    </div>
  );
}
