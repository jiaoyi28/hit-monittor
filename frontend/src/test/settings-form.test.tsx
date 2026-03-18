import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { SettingsForm } from "../components/settings/settings-form";


describe("SettingsForm", () => {
  it("submits sync and analysis intervals", async () => {
    const user = userEvent.setup();

    render(
      <SettingsForm
        initialValues={{ syncIntervalMinutes: 60, analysisIntervalMinutes: 240 }}
        onSubmit={async () => {}}
      />,
    );

    const syncInput = screen.getByLabelText("抓取间隔（分钟）");
    await user.clear(syncInput);
    await user.type(syncInput, "30");

    expect(screen.getByDisplayValue("30")).toBeInTheDocument();
    expect(screen.getByDisplayValue("240")).toBeInTheDocument();
  });
});
