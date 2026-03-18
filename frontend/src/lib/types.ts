export type HotItem = {
  title: string;
  url: string;
  summary?: string | null;
};

export type DashboardResponse = {
  hot_issues: HotItem[];
  hot_pull_requests: HotItem[];
  latest_releases: HotItem[];
};

export type RepositoryListItem = {
  id: number;
  full_name: string;
  description?: string | null;
  html_url: string;
  enabled: boolean;
};

export type RepositoryCreateRequest = {
  url: string;
};

export type RepositoryDetailResponse = {
  repository: {
    id: number;
    full_name: string;
    description?: string | null;
    html_url: string;
  };
  issues: HotItem[];
  pull_requests: HotItem[];
  releases: HotItem[];
};

export type SettingsResponse = {
  sync_interval_minutes: number;
  analysis_interval_minutes: number;
};

export type SettingsUpdate = Partial<SettingsResponse>;
