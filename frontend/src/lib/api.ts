import type {
  DashboardResponse,
  RepositoryCreateRequest,
  RepositoryDetailResponse,
  RepositoryListItem,
  SettingsResponse,
  SettingsUpdate,
} from "./types";

async function request<T>(input: string, init?: RequestInit): Promise<T> {
  const response = await fetch(input, init);

  if (!response.ok) {
    throw new Error(`Request failed for ${input}`);
  }

  return response.json() as Promise<T>;
}

export async function getDashboard(): Promise<DashboardResponse> {
  return request<DashboardResponse>("/api/dashboard");
}

export async function getRepositories(): Promise<RepositoryListItem[]> {
  return request<RepositoryListItem[]>("/api/repositories");
}

export async function addRepository(payload: RepositoryCreateRequest): Promise<RepositoryListItem> {
  return request<RepositoryListItem>("/api/repositories", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function getRepositoryDetail(repositoryId: number): Promise<RepositoryDetailResponse> {
  return request<RepositoryDetailResponse>(`/api/repositories/${repositoryId}`);
}

export async function getSettings(): Promise<SettingsResponse> {
  return request<SettingsResponse>("/api/settings");
}

export async function updateSettings(payload: SettingsUpdate): Promise<SettingsResponse> {
  return request<SettingsResponse>("/api/settings", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
