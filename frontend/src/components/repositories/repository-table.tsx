import type { RepositoryListItem } from "../../lib/types";
import { Badge } from "../ui/badge";
import { Card } from "../ui/card";
import { Input } from "../ui/input";


type RepositoryTableProps = {
  repositories: RepositoryListItem[];
  keyword: string;
  onKeywordChange: (value: string) => void;
};

export function RepositoryTable({ repositories, keyword, onKeywordChange }: RepositoryTableProps) {
  const filtered = repositories.filter((repository) =>
    repository.full_name.toLowerCase().includes(keyword.toLowerCase()),
  );

  return (
    <Card className="space-y-5">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.22em] text-muted">Watchlist</p>
          <h2 className="mt-2 font-display text-3xl">仓库观察清单</h2>
        </div>
        <div className="w-full md:max-w-xs">
          <label className="mb-2 block text-sm font-semibold text-ink" htmlFor="repository-filter">
            筛选仓库
          </label>
          <Input
            id="repository-filter"
            onChange={(event) => onKeywordChange(event.target.value)}
            placeholder="例如 openai/openai-python"
            value={keyword}
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-[24px] border border-line">
        <table className="min-w-full border-collapse text-left text-sm">
          <thead className="bg-[#efe6d9] text-muted">
            <tr>
              <th className="px-5 py-4 font-semibold">仓库</th>
              <th className="px-5 py-4 font-semibold">状态</th>
              <th className="px-5 py-4 font-semibold">描述</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((repository) => (
              <tr className="border-t border-line bg-white/70" key={repository.id}>
                <td className="px-5 py-4">
                  <a className="font-semibold text-ink hover:text-signal" href={`#/repositories/${repository.id}`}>
                    {repository.full_name}
                  </a>
                </td>
                <td className="px-5 py-4">
                  <Badge className={repository.enabled ? "" : "border-line bg-white text-muted"}>
                    {repository.enabled ? "tracking" : "paused"}
                  </Badge>
                </td>
                <td className="px-5 py-4 text-muted">{repository.description ?? "暂无描述"}</td>
              </tr>
            ))}
            {filtered.length === 0 ? (
              <tr>
                <td className="px-5 py-8 text-muted" colSpan={3}>
                  没有匹配的仓库。
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
