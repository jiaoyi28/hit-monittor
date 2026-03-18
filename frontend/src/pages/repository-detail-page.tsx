import { useEffect, useState } from "react";

import { DetailSections } from "../components/repository-detail/detail-sections";
import { Badge } from "../components/ui/badge";
import { Card } from "../components/ui/card";
import { getRepositoryDetail } from "../lib/api";
import type { RepositoryDetailResponse } from "../lib/types";


type RepositoryDetailPageProps = {
  repositoryId: number;
};

export function RepositoryDetailPage({ repositoryId }: RepositoryDetailPageProps) {
  const [data, setData] = useState<RepositoryDetailResponse | null>(null);

  useEffect(() => {
    void getRepositoryDetail(repositoryId).then(setData);
  }, [repositoryId]);

  if (!data) {
    return <Card>正在加载仓库详情...</Card>;
  }

  return (
    <div className="space-y-6">
      <Card className="space-y-4">
        <Badge>Repository Brief</Badge>
        <div className="space-y-3">
          <h2 className="font-display text-4xl">{data.repository.full_name}</h2>
          <p className="max-w-3xl text-sm leading-7 text-muted">{data.repository.description ?? "暂无描述"}</p>
          <a className="inline-flex text-sm font-semibold text-signal underline-offset-4 hover:underline" href={data.repository.html_url}>
            打开 GitHub 原始页面
          </a>
        </div>
      </Card>

      <div className="grid gap-6 xl:grid-cols-3">
        <DetailSections items={data.issues} title="热点 Issues" />
        <DetailSections items={data.pull_requests} title="热点 PRs" />
        <DetailSections items={data.releases} title="最新 Releases" />
      </div>
    </div>
  );
}
