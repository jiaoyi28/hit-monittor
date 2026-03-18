import { useEffect, useState } from "react";

import { SettingsForm } from "../components/settings/settings-form";
import { Card } from "../components/ui/card";
import { getSettings, updateSettings } from "../lib/api";
import type { SettingsResponse, SettingsUpdate } from "../lib/types";


export function SettingsPage() {
  const [settings, setSettings] = useState<SettingsResponse | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void getSettings()
      .then((payload) => {
        setSettings(payload);
        setError(null);
      })
      .catch(() => {
        setError("配置加载失败，请确认后端服务已启动。");
      });
  }, []);

  async function handleSubmit(payload: SettingsUpdate) {
    try {
      const next = await updateSettings(payload);
      setSettings(next);
      setStatus("配置已更新。");
      setError(null);
    } catch {
      setStatus(null);
      setError("配置保存失败，请稍后重试。");
    }
  }

  if (!settings) {
    if (error) {
      return <Card className="border-red-200 bg-red-50 text-red-700 shadow-none">{error}</Card>;
    }

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
      {error ? (
        <Card className="rounded-[20px] border-red-200 bg-red-50 py-4 text-sm text-red-700 shadow-none">{error}</Card>
      ) : null}
    </div>
  );
}
