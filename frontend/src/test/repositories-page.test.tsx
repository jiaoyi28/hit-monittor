import "@testing-library/jest-dom/vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";

import { RepositoriesPage } from "../pages/repositories-page";


describe("RepositoriesPage", () => {
  it("adds a repository from a GitHub URL and renders it in the watchlist", async () => {
    const user = userEvent.setup();
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          full_name: "openai/openai-python",
          description: "Python library for the OpenAI API",
          html_url: "https://github.com/openai/openai-python",
          enabled: true,
        }),
      });

    vi.stubGlobal("fetch", fetchMock);

    render(<RepositoriesPage />);

    await user.type(screen.getByLabelText("GitHub 仓库 URL"), "https://github.com/openai/openai-python");
    await user.click(screen.getByRole("button", { name: "添加仓库" }));

    await waitFor(() => expect(screen.getByText("openai/openai-python")).toBeInTheDocument());
    expect(screen.getByText("仓库已加入观察清单，并已立即同步。")).toBeInTheDocument();
  });
});
