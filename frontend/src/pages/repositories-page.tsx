import { useEffect, useState } from "react";

import { RepositoryTable } from "../components/repositories/repository-table";
import { getRepositories } from "../lib/api";
import type { RepositoryListItem } from "../lib/types";


export function RepositoriesPage() {
  const [repositories, setRepositories] = useState<RepositoryListItem[]>([]);
  const [keyword, setKeyword] = useState("");

  useEffect(() => {
    void getRepositories().then(setRepositories);
  }, []);

  return <RepositoryTable keyword={keyword} onKeywordChange={setKeyword} repositories={repositories} />;
}
