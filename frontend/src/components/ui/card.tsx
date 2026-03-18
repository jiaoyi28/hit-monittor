import type { HTMLAttributes } from "react";

import { cn } from "../../lib/utils";


export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-[28px] border border-line bg-panel p-6 shadow-[var(--shadow)] backdrop-blur-sm",
        className,
      )}
      {...props}
    />
  );
}
