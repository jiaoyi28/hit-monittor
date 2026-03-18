import type { InputHTMLAttributes } from "react";

import { cn } from "../../lib/utils";


export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "w-full rounded-2xl border border-line bg-white/80 px-4 py-3 text-sm text-ink outline-none transition placeholder:text-muted focus:border-signal/50 focus:bg-white",
        className,
      )}
      {...props}
    />
  );
}
