import {
  AlertTriangle,
  Ban,
  Lightbulb,
  MessageSquareWarning,
  Sparkles,
  Table2,
} from "lucide-react";
import { cn } from "@/lib/utils";

function CalloutShell({
  title,
  icon,
  className,
  children,
}: {
  title: string;
  icon: React.ReactNode;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <aside
      className={cn(
        "my-6 rounded-xl border px-4 py-3.5 text-[15px] leading-7",
        className,
      )}
      role="note"
    >
      <div className="mb-1.5 flex items-center gap-2 text-sm font-semibold tracking-tight text-white">
        {icon}
        <span>{title}</span>
      </div>
      <div className="text-[#d7dbe3] [&>p]:m-0 [&>p+p]:mt-2">{children}</div>
    </aside>
  );
}

export function Tip({ children }: { children: React.ReactNode }) {
  return (
    <CalloutShell
      title="Tip"
      icon={<Lightbulb className="h-4 w-4" aria-hidden />}
      className="border-teal-500/30 bg-teal-500/10"
    >
      {children}
    </CalloutShell>
  );
}

export function Warning({ children }: { children: React.ReactNode }) {
  return (
    <CalloutShell
      title="Warning"
      icon={<AlertTriangle className="h-4 w-4" aria-hidden />}
      className="border-amber-500/40 bg-amber-500/10"
    >
      {children}
    </CalloutShell>
  );
}

export function Trick({ children }: { children: React.ReactNode }) {
  return (
    <CalloutShell
      title="Trick"
      icon={<Sparkles className="h-4 w-4" aria-hidden />}
      className="border-sky-500/30 bg-sky-500/10"
    >
      {children}
    </CalloutShell>
  );
}

export function InterviewNote({ children }: { children: React.ReactNode }) {
  return (
    <CalloutShell
      title="Interview note"
      icon={<MessageSquareWarning className="h-4 w-4" aria-hidden />}
      className="border-indigo-500/30 bg-indigo-500/10"
    >
      {children}
    </CalloutShell>
  );
}

export function Pitfall({ children }: { children: React.ReactNode }) {
  return (
    <CalloutShell
      title="Pitfall"
      icon={<Ban className="h-4 w-4" aria-hidden />}
      className="border-rose-500/30 bg-rose-500/10"
    >
      {children}
    </CalloutShell>
  );
}

export function ComplexityTable({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <CalloutShell
      title="Complexity"
      icon={<Table2 className="h-4 w-4" aria-hidden />}
      className="border-border bg-muted/50"
    >
      <div className="overflow-x-auto">{children}</div>
    </CalloutShell>
  );
}

export function Visualizer({
  title = "Visualizer",
  children,
}: {
  title?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="my-6 rounded-lg border border-dashed border-border bg-muted/30 p-4">
      <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        {title}
      </p>
      {children}
    </div>
  );
}
