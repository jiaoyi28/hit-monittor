import { useState, type FormEvent } from "react";

import { Button } from "../ui/button";
import { Card } from "../ui/card";
import { Input } from "../ui/input";


type RepositoryAddFormProps = {
  onSubmit: (url: string) => Promise<void>;
};

export function RepositoryAddForm({ onSubmit }: RepositoryAddFormProps) {
  const [url, setUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit(url);
      setUrl("");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Card className="border-signal/15 bg-[linear-gradient(135deg,rgba(255,248,242,0.96),rgba(255,255,255,0.92))]">
      <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-2xl space-y-2">
          <p className="text-xs uppercase tracking-[0.22em] text-muted">Quick Add</p>
          <div className="space-y-2">
            <h2 className="font-display text-3xl text-ink">添加 GitHub 观察仓库</h2>
            <p className="text-sm leading-6 text-muted">
              输入公开仓库 URL，系统会立即拉取仓库信息，并把它加入当前观察清单。
            </p>
          </div>
        </div>
        <form className="grid w-full gap-3 lg:max-w-2xl lg:grid-cols-[1fr_auto]" onSubmit={handleSubmit}>
          <label className="space-y-2">
            <span className="block text-sm font-semibold text-ink">GitHub 仓库 URL</span>
            <Input
              aria-label="GitHub 仓库 URL"
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://github.com/openai/openai-python"
              value={url}
            />
          </label>
          <Button className="self-end" disabled={submitting || url.trim() === ""} type="submit">
            {submitting ? "正在同步..." : "添加仓库"}
          </Button>
        </form>
      </div>
    </Card>
  );
}
