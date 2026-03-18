import { useState } from "react";
import { ArrowUpRight, Flame, GitPullRequestArrow, Sparkles } from "lucide-react";

import type { DashboardResponse, HotItem } from "../../lib/types";
import { Badge } from "../ui/badge";
import { Card } from "../ui/card";


type SummaryCardsProps = {
  data: DashboardResponse;
};

type SectionKey = "issues" | "pullRequests" | "releases";

type SectionDefinition = {
  key: SectionKey;
  title: string;
  eyebrow: string;
  description: string;
  items: HotItem[];
};

function FeaturedItems({ items, title }: { items: HotItem[]; title: string }) {
  if (items.length === 0) {
    return (
      <div className="rounded-[24px] border border-dashed border-line bg-white/55 p-6 text-sm leading-7 text-muted">
        当前没有可展示的 {title} 数据。
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {items.map((item) => (
        <a
          key={`${title}-${item.title}`}
          className="block rounded-[24px] border border-line bg-white/72 p-5 transition hover:-translate-y-0.5 hover:border-signal/40"
          href={item.url}
          rel="noreferrer"
          target="_blank"
        >
          <div className="flex items-start justify-between gap-4">
            <p className="font-semibold text-ink">{item.title}</p>
            <ArrowUpRight className="mt-0.5 size-4 shrink-0 text-signal" />
          </div>
          {item.summary ? <p className="mt-2 text-sm leading-7 text-muted">{item.summary}</p> : null}
        </a>
      ))}
    </div>
  );
}

export function SummaryCards({ data }: SummaryCardsProps) {
  const [activeSection, setActiveSection] = useState<SectionKey>("issues");
  const totalEvents = data.hot_issues.length + data.hot_pull_requests.length + data.latest_releases.length;
  const sections: SectionDefinition[] = [
    {
      key: "issues",
      title: "热点 Issues",
      eyebrow: "Issue Watch",
      description: "优先关注讨论密度最高、最值得判断是否需要介入的问题线程。",
      items: data.hot_issues,
    },
    {
      key: "pullRequests",
      title: "热点 PRs",
      eyebrow: "PR Focus",
      description: "集中查看当前推进中的合并请求，快速判断评审和合并节奏。",
      items: data.hot_pull_requests,
    },
    {
      key: "releases",
      title: "最新 Releases",
      eyebrow: "Release Watch",
      description: "按发布时间追踪新版本与变更摘要，避免错过关键发布。",
      items: data.latest_releases,
    },
  ];
  const activePanel = sections.find((section) => section.key === activeSection) ?? sections[0];

  return (
    <div className="space-y-6">
      <Card className="overflow-hidden">
        <div className="grid gap-5 lg:grid-cols-[1.4fr_1fr]">
          <div className="space-y-4">
            <Badge>Monitor Desk</Badge>
            <div className="space-y-3">
              <h2 className="font-display text-4xl leading-tight text-ink md:text-5xl">
                把 GitHub 杂音压缩成一个可读的观察面板。
              </h2>
              <p className="max-w-2xl text-sm leading-7 text-muted md:text-base">
                这是一个偏编辑台风格的总览页。优先展示最值得点开的 issue、PR 和 release，而不是堆原始列表。
              </p>
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-3 lg:grid-cols-1">
            <Card className="rounded-[22px] bg-signal text-white shadow-none">
              <Flame className="mb-5 size-6" />
              <p className="text-xs uppercase tracking-[0.22em] text-white/70">Events</p>
              <p className="mt-2 font-display text-4xl">{totalEvents}</p>
            </Card>
            <Card className="rounded-[22px] shadow-none">
              <GitPullRequestArrow className="mb-5 size-6 text-signal" />
              <p className="text-xs uppercase tracking-[0.22em] text-muted">PR Focus</p>
              <p className="mt-2 font-display text-3xl">{data.hot_pull_requests.length}</p>
            </Card>
            <Card className="rounded-[22px] shadow-none">
              <Sparkles className="mb-5 size-6 text-signal" />
              <p className="text-xs uppercase tracking-[0.22em] text-muted">Release Watch</p>
              <p className="mt-2 font-display text-3xl">{data.latest_releases.length}</p>
            </Card>
          </div>
        </div>
      </Card>

      <Card className="overflow-hidden">
        <div className="grid gap-6 lg:grid-cols-[240px_minmax(0,1fr)]">
          <div
            aria-label="总览栏目切换"
            aria-orientation="vertical"
            className="flex flex-col gap-3"
            role="tablist"
          >
            {sections.map((section) => {
              const selected = section.key === activePanel.key;
              return (
                <button
                  key={section.key}
                  aria-controls={`dashboard-panel-${section.key}`}
                  aria-selected={selected}
                  className={[
                    "rounded-[22px] border px-4 py-4 text-left transition",
                    selected
                      ? "border-signal bg-signal-soft text-ink shadow-[0_12px_30px_rgba(200,76,47,0.12)]"
                      : "border-line bg-white/45 text-muted hover:border-signal/30 hover:bg-white/70",
                  ].join(" ")}
                  id={`dashboard-tab-${section.key}`}
                  onClick={() => setActiveSection(section.key)}
                  role="tab"
                  type="button"
                >
                  <p className="text-xs uppercase tracking-[0.2em]">{section.eyebrow}</p>
                  <p className="mt-2 font-display text-2xl text-ink">{section.title}</p>
                  <p className="mt-2 text-sm leading-6">{section.items.length} 条</p>
                </button>
              );
            })}
          </div>

          <section
            aria-labelledby={`dashboard-tab-${activePanel.key}`}
            className="space-y-5"
            id={`dashboard-panel-${activePanel.key}`}
            role="tabpanel"
          >
            <div className="rounded-[24px] border border-line bg-white/55 p-5">
              <p className="text-xs uppercase tracking-[0.22em] text-muted">{activePanel.eyebrow}</p>
              <div className="mt-3 space-y-3">
                <h3 className="font-display text-3xl text-ink">{activePanel.title}</h3>
                <p className="max-w-2xl text-sm leading-7 text-muted">{activePanel.description}</p>
              </div>
            </div>

            <FeaturedItems items={activePanel.items} title={activePanel.title} />
          </section>
        </div>
      </Card>
    </div>
  );
}
