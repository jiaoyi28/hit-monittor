import { useState, type FormEvent } from "react";

import type { SettingsUpdate } from "../../lib/types";
import { Button } from "../ui/button";
import { Card } from "../ui/card";
import { Input } from "../ui/input";


type SettingsFormProps = {
  initialValues: {
    syncIntervalMinutes: number;
    analysisIntervalMinutes: number;
  };
  onSubmit: (payload: SettingsUpdate) => Promise<void>;
};

export function SettingsForm({ initialValues, onSubmit }: SettingsFormProps) {
  const [syncIntervalMinutes, setSyncIntervalMinutes] = useState(String(initialValues.syncIntervalMinutes));
  const [analysisIntervalMinutes, setAnalysisIntervalMinutes] = useState(String(initialValues.analysisIntervalMinutes));
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit({
        sync_interval_minutes: Number(syncIntervalMinutes),
        analysis_interval_minutes: Number(analysisIntervalMinutes),
      });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Card className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.22em] text-muted">Runtime</p>
        <h2 className="mt-2 font-display text-3xl">抓取与分析频率</h2>
      </div>
      <form className="grid gap-5 md:grid-cols-2" onSubmit={handleSubmit}>
        <label className="space-y-2">
          <span className="block text-sm font-semibold text-ink">抓取间隔（分钟）</span>
          <Input
            aria-label="抓取间隔（分钟）"
            inputMode="numeric"
            onChange={(event) => setSyncIntervalMinutes(event.target.value)}
            value={syncIntervalMinutes}
          />
        </label>
        <label className="space-y-2">
          <span className="block text-sm font-semibold text-ink">分析间隔（分钟）</span>
          <Input
            aria-label="分析间隔（分钟）"
            inputMode="numeric"
            onChange={(event) => setAnalysisIntervalMinutes(event.target.value)}
            value={analysisIntervalMinutes}
          />
        </label>
        <div className="md:col-span-2">
          <Button disabled={submitting} type="submit">
            {submitting ? "保存中..." : "保存设置"}
          </Button>
        </div>
      </form>
    </Card>
  );
}
