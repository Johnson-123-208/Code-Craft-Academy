import Link from "next/link";
import { DifficultyText } from "@/components/leetcode/difficulty";
import type { ProblemSummary } from "@/types/content";
import { cn } from "@/lib/utils";

export function ProblemListTable({
  problems,
}: {
  problems: ProblemSummary[];
}) {
  return (
    <div className="overflow-hidden rounded-xl border border-[#333] bg-[#262626] shadow-xl">
      <div className="grid grid-cols-[56px_1fr_100px_1fr] gap-2 border-b border-[#333] bg-[#2a2a2a] px-4 py-3 text-xs font-semibold uppercase tracking-wide text-[#eff1f699]">
        <span>#</span>
        <span>Title</span>
        <span>Difficulty</span>
        <span className="hidden sm:block">Topics</span>
      </div>
      <ul>
        {problems.map((problem, i) => (
          <li key={problem.slug}>
            <Link
              href={`/practice/${problem.slug}`}
              className={cn(
                "grid grid-cols-[56px_1fr_100px_1fr] gap-2 px-4 py-3.5 text-sm transition hover:bg-[#333]/70",
                i % 2 === 0 ? "bg-[#262626]" : "bg-[#1f1f1f]",
              )}
            >
              <span className="font-mono text-[#eff1f666]">{i + 1}</span>
              <span className="truncate font-medium text-[#eff1f6] hover:text-[#ffa116]">
                {problem.title}
              </span>
              <DifficultyText difficulty={problem.difficulty} />
              <span className="hidden truncate text-[#eff1f666] sm:block">
                {problem.topics.slice(0, 3).join(", ")}
              </span>
            </Link>
          </li>
        ))}
      </ul>
      {problems.length === 0 && (
        <p className="px-4 py-10 text-center text-sm text-[#eff1f699]">
          No problems match those filters.
        </p>
      )}
    </div>
  );
}
