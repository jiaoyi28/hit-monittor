import "@testing-library/jest-dom/vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";

import { DashboardPage } from "../pages/dashboard-page";


describe("DashboardPage", () => {
  it("switches between issue, pr, and release panels", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          hot_issues: [{ title: "Issue Alpha", url: "https://example.com/issues/1", summary: "Issue summary" }],
          hot_pull_requests: [{ title: "PR Beta", url: "https://example.com/pr/1", summary: "PR summary" }],
          latest_releases: [{ title: "v1.0.0", url: "https://example.com/releases/1", summary: "Release summary" }],
        }),
      }),
    );

    render(<DashboardPage />);
    const user = userEvent.setup();

    expect(await screen.findByRole("tab", { name: /热点 Issues/ })).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Issue Alpha")).toBeInTheDocument());
    expect(screen.queryByText("PR Beta")).not.toBeInTheDocument();

    await user.click(screen.getByRole("tab", { name: /热点 PRs/ }));
    expect(await screen.findByText("PR Beta")).toBeInTheDocument();
    expect(screen.queryByText("Issue Alpha")).not.toBeInTheDocument();

    await user.click(screen.getByRole("tab", { name: /最新 Releases/ }));
    expect(await screen.findByText("v1.0.0")).toBeInTheDocument();
    expect(screen.queryByText("PR Beta")).not.toBeInTheDocument();
  });
});
