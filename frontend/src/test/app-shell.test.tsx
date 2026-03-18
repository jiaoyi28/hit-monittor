import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";

import { AppShell } from "../components/layout/app-shell";


describe("AppShell", () => {
  it("renders navigation links", () => {
    render(<AppShell />);

    expect(screen.getByText("总览")).toBeInTheDocument();
    expect(screen.getByText("配置")).toBeInTheDocument();
  });
});
