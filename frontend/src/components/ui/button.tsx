import { cva, type VariantProps } from "class-variance-authority";
import type { ButtonHTMLAttributes } from "react";

import { cn } from "../../lib/utils";


const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-full border px-4 py-2 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-signal/40 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "border-signal bg-signal text-white shadow-[0_10px_24px_rgba(200,76,47,0.24)] hover:-translate-y-0.5",
        secondary: "border-line bg-panel-strong text-ink hover:border-signal/40 hover:bg-white",
        ghost: "border-transparent bg-transparent text-muted hover:bg-signal-soft hover:text-ink",
      },
    },
    defaultVariants: {
      variant: "primary",
    },
  },
);

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & VariantProps<typeof buttonVariants>;

export function Button({ className, variant, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant }), className)} {...props} />;
}
