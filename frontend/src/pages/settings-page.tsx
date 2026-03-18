import { useEffect, useState } from "react";

import { SettingsForm } from "../components/settings/settings-form";
import { Card } from "../components/ui/card";
import { getSettings, updateSettings } from "../lib/api";
import type { SettingsResponse, SettingsUpdate } from "../lib/types";


export function SettingsPage() {
  const [settings, setSettings] = useState<SettingsResponse | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    void getSettings().then(setSettings);
  }, []);

  async function handleSubmit(payload: SettingsUpdate) {
    const next = await updateSettings(payload);
    setSettings(next);
    setStatus("设置已更新。");
  }

  if (!settings) {
    return <Card>正在加载配置...</Card>;
  }

  return (
    <div className="space-y-4">
      <SettingsForm
        initialValues={{
          syncIntervalMinutes: settings.sync_interval_minutes,
          analysisIntervalMinutes: settings.analysis_interval_minutes,
        }}
        onSubmit={handleSubmit}
      />
      {status ? (
        <Card className="rounded-[20px] border-signal/20 bg-signal-soft/70 py-4 text-sm text-signal shadow-none">
          {status}
        </Card>
      ) : null}
    </div>
  );
}
