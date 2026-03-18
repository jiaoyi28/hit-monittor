import { useEffect, useState } from "react";

import { RepositoryAddForm } from "../components/repositories/repository-add-form";
import { RepositoryTable } from "../components/repositories/repository-table";
import { Card } from "../components/ui/card";
import { addRepository, getRepositories } from "../lib/api";
import type { RepositoryListItem } from "../lib/types";


export function RepositoriesPage() {
  const [repositories, setRepositories] = useState<RepositoryListItem[]>([]);
  const [keyword, setKeyword] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void getRepositories()
      .then(setRepositories)
      .catch(() => setError("仓库列表加载失败，请确认后端服务已启动。"));
  }, []);

  async function handleAddRepository(url: string) {
    try {
      const repository = await addRepository({ url });
      setRepositories((current) => {
        const filtered = current.filter((item) => item.id !== repository.id);
        return [...filtered, repository].sort((left, right) => left.id - right.id);
      });
      setStatus("仓库已加入观察清单，并已立即同步。");
      setError(null);
    } catch {
      setStatus(null);
      setError("添加失败，请输入有效的 GitHub 公开仓库 URL。");
    }
  }

  return (
    <div className="space-y-4">
      <RepositoryAddForm onSubmit={handleAddRepository} />
      {status ? (
        <Card className="rounded-[20px] border-signal/20 bg-signal-soft/70 py-4 text-sm text-signal shadow-none">
          {status}
        </Card>
      ) : null}
      {error ? (
        <Card className="rounded-[20px] border-red-200 bg-red-50 py-4 text-sm text-red-700 shadow-none">
          {error}
        </Card>
      ) : null}
      <RepositoryTable keyword={keyword} onKeywordChange={setKeyword} repositories={repositories} />
    </div>
  );
}
