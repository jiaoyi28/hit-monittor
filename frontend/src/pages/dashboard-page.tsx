import { useEffect, useState } from "react";

import { getDashboard } from "../lib/api";
import type { DashboardResponse } from "../lib/types";
import { SummaryCards } from "../components/dashboard/summary-cards";


export function DashboardPage() {
  const [data, setData] = useState<DashboardResponse>({
    hot_issues: [],
    hot_pull_requests: [],
    latest_releases: [],
  });

  useEffect(() => {
    void getDashboard().then(setData);
  }, []);

  return <SummaryCards data={data} />;
}
