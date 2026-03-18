import { ArrowUpRight, Flame, GitPullRequestArrow, Sparkles } from "lucide-react";

import type { DashboardResponse, HotItem } from "../../lib/types";
import { Badge } from "../ui/badge";
import { Card } from "../ui/card";


type SummaryCardsProps = {
  data: DashboardResponse;
};

function FeaturedList({ title, items }: { title: string; items: HotItem[] }) {
  return (
    <Card className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-display text-xl">{title}</h3>
        <ArrowUpRight className="size-4 text-signal" />
      </div>
      <div className="space-y-3">
        {items.length === 0 ? <p className="text-sm text-muted">当前没有可展示的数据。</p> : null}
        {items.map((item) => (
          <a
            key={`${title}-${item.title}`}
            className="block rounded-2xl border border-line bg-white/70 p-4 transition hover:-translate-y-0.5 hover:border-signal/40"
            href={item.url}
            rel="noreferrer"
            target="_blank"
          >
            <p className="font-semibold text-ink">{item.title}</p>
            {item.summary ? <p className="mt-1 text-sm leading-6 text-muted">{item.summary}</p> : null}
          </a>
        ))}
      </div>
    </Card>
  );
}

export function SummaryCards({ data }: SummaryCardsProps) {
  const totalEvents = data.hot_issues.length + data.hot_pull_requests.length + data.latest_releases.length;

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

      <div className="grid gap-6 xl:grid-cols-3">
        <FeaturedList title="热点 Issues" items={data.hot_issues} />
        <FeaturedList title="热点 PRs" items={data.hot_pull_requests} />
        <FeaturedList title="最新 Releases" items={data.latest_releases} />
      </div>
    </div>
  );
}
