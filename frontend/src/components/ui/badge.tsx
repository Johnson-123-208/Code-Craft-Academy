import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary/10 text-primary",
        secondary: "border-transparent bg-secondary text-secondary-foreground",
        outline: "text-foreground",
        beginner: "border-transparent bg-emerald-500/15 text-emerald-700 dark:text-emerald-300",
        intermediate: "border-transparent bg-amber-500/15 text-amber-800 dark:text-amber-300",
        advanced: "border-transparent bg-rose-500/15 text-rose-700 dark:text-rose-300",
        easy: "border-transparent bg-[#00b8a3]/15 text-[#00b8a3]",
        medium: "border-transparent bg-[#ffc01e]/15 text-[#ffc01e]",
        hard: "border-transparent bg-[#ff375f]/15 text-[#ff375f]",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}
