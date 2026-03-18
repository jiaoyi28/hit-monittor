import "@testing-library/jest-dom/vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import { SettingsPage } from "../pages/settings-page";


describe("SettingsPage", () => {
  it("renders interval fields after loading settings", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          sync_interval_minutes: 60,
          analysis_interval_minutes: 240,
        }),
      }),
    );

    render(<SettingsPage />);

    expect(await screen.findByLabelText("抓取间隔（分钟）")).toBeInTheDocument();
    expect(screen.getByDisplayValue("60")).toBeInTheDocument();
    expect(screen.getByDisplayValue("240")).toBeInTheDocument();
  });

  it("shows an error message when loading settings fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
      }),
    );

    render(<SettingsPage />);

    await waitFor(() => {
      expect(screen.getByText("配置加载失败，请确认后端服务已启动。")).toBeInTheDocument();
    });
  });
});
