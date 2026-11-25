import { cn } from "@/lib/utils";

const STYLES: Record<string, string> = {
  easy: "text-[#00b8a3]",
  medium: "text-[#ffc01e]",
  hard: "text-[#ff375f]",
  beginner: "text-[#00b8a3]",
  intermediate: "text-[#ffc01e]",
  advanced: "text-[#ff375f]",
};

export function DifficultyText({
  difficulty,
  className,
}: {
  difficulty: string;
  className?: string;
}) {
  const key = difficulty.toLowerCase();
  const label =
    key.charAt(0).toUpperCase() + key.slice(1);
  return (
    <span className={cn("text-sm font-medium", STYLES[key] ?? "text-muted-foreground", className)}>
      {label}
    </span>
  );
}
