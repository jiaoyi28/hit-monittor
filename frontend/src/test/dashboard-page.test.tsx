import "@testing-library/jest-dom/vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import { DashboardPage } from "../pages/dashboard-page";


describe("DashboardPage", () => {
  it("shows hot issue and release sections", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          hot_issues: [{ title: "Issue A", url: "https://example.com/issues/1", summary: "Issue summary" }],
          hot_pull_requests: [{ title: "PR A", url: "https://example.com/pr/1", summary: "PR summary" }],
          latest_releases: [{ title: "v1.0.0", url: "https://example.com/releases/1", summary: "Release summary" }],
        }),
      }),
    );

    render(<DashboardPage />);

    expect(await screen.findByText("热点 Issues")).toBeInTheDocument();
    expect(await screen.findByText("最新 Releases")).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Issue A")).toBeInTheDocument());
  });
});
