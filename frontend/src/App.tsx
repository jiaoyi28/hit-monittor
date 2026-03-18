import { useEffect, useState } from "react";

import { AppShell } from "./components/layout/app-shell";
import { DashboardPage } from "./pages/dashboard-page";
import { RepositoriesPage } from "./pages/repositories-page";
import { RepositoryDetailPage } from "./pages/repository-detail-page";
import { SettingsPage } from "./pages/settings-page";

type Route =
  | { kind: "dashboard" }
  | { kind: "repositories" }
  | { kind: "repository-detail"; repositoryId: number }
  | { kind: "settings" };

function parseHash(hash: string): Route {
  const normalized = hash.replace(/^#/, "") || "/";

  if (normalized === "/" || normalized === "") {
    return { kind: "dashboard" };
  }

  if (normalized === "/repositories") {
    return { kind: "repositories" };
  }

  if (normalized.startsWith("/repositories/")) {
    const repositoryId = Number(normalized.split("/")[2]);
    return { kind: "repository-detail", repositoryId };
  }

  if (normalized === "/settings") {
    return { kind: "settings" };
  }

  return { kind: "dashboard" };
}

export default function App() {
  const [route, setRoute] = useState<Route>(() => parseHash(window.location.hash));

  useEffect(() => {
    function handleHashChange() {
      setRoute(parseHash(window.location.hash));
    }

    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  if (route.kind === "repositories") {
    return (
      <AppShell heading="围绕你的观察清单组织 GitHub 仓库。" kicker="Repository Watch">
        <RepositoriesPage />
      </AppShell>
    );
  }

  if (route.kind === "repository-detail") {
    return (
      <AppShell heading="把单仓库的热点拆成可快速扫读的三栏。" kicker="Repository Detail">
        <RepositoryDetailPage repositoryId={route.repositoryId} />
      </AppShell>
    );
  }

  if (route.kind === "settings") {
    return (
      <AppShell heading="把抓取和分析节奏调到你愿意长期看的频率。" kicker="Settings">
        <SettingsPage />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <DashboardPage />
    </AppShell>
  );
}
