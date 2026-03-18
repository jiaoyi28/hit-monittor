import type { HotItem } from "../../lib/types";
import { Card } from "../ui/card";


type DetailSectionsProps = {
  title: string;
  items: HotItem[];
};

export function DetailSections({ title, items }: DetailSectionsProps) {
  return (
    <Card className="space-y-4">
      <h3 className="font-display text-2xl">{title}</h3>
      <div className="space-y-3">
        {items.length === 0 ? <p className="text-sm text-muted">当前没有数据。</p> : null}
        {items.map((item) => (
          <a
            key={`${title}-${item.title}`}
            className="block rounded-2xl border border-line bg-white/70 p-4 transition hover:-translate-y-0.5 hover:border-signal/40"
            href={item.url}
            rel="noreferrer"
            target="_blank"
          >
            <p className="font-semibold text-ink">{item.title}</p>
            {item.summary ? <p className="mt-2 text-sm leading-6 text-muted">{item.summary}</p> : null}
          </a>
        ))}
      </div>
    </Card>
  );
}
