import { ProblemListTable } from "@/components/leetcode/problem-list";
import { listProblems } from "@/lib/content";

export const metadata = {
  title: "Problem List",
  description: "LeetCode-style problemset — filter by topic, difficulty, and company.",
};

export default function PracticePage({
  searchParams,
}: {
  searchParams?: { topic?: string; difficulty?: string; company?: string; q?: string };
}) {
  let problems = listProblems({
    topic: searchParams?.topic,
    difficulty: searchParams?.difficulty,
    company: searchParams?.company,
  });

  const q = searchParams?.q?.trim().toLowerCase();
  if (q) {
    problems = problems.filter(
      (p) =>
        p.title.toLowerCase().includes(q) ||
        p.slug.toLowerCase().includes(q) ||
        p.topics.some((t) => t.toLowerCase().includes(q)),
    );
  }

  const all = listProblems();
  const topics = Array.from(new Set(all.flatMap((p) => p.topics))).sort();
  const companies = Array.from(new Set(all.flatMap((p) => p.company_tags))).sort();

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#1a1a1a] text-[#eff1f6]">
      <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#ffa116]">
              Problemset
            </p>
            <h1 className="mt-1 text-3xl font-semibold tracking-tight text-white">
              Practice
            </h1>
            <p className="mt-2 text-sm text-[#eff1f699]">
              {problems.length} problems · LeetCode-style workspace
            </p>
          </div>
        </div>

        <form
          className="mb-6 flex flex-wrap items-center gap-2 rounded-xl border border-[#333] bg-[#262626] p-3"
          method="get"
        >
          <input
            name="q"
            defaultValue={searchParams?.q ?? ""}
            placeholder="Search title or topic…"
            className="h-9 min-w-[200px] flex-1 rounded-lg border border-[#333] bg-[#1a1a1a] px-3 text-sm text-white placeholder:text-[#eff1f666] focus:border-[#ffa116] focus:outline-none"
          />
          <select
            name="difficulty"
            defaultValue={searchParams?.difficulty ?? ""}
            className="h-9 rounded-lg border border-[#333] bg-[#1a1a1a] px-3 text-sm text-white"
          >
            <option value="">Difficulty</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
          <select
            name="topic"
            defaultValue={searchParams?.topic ?? ""}
            className="h-9 max-w-[160px] rounded-lg border border-[#333] bg-[#1a1a1a] px-3 text-sm text-white"
          >
            <option value="">Topic</option>
            {topics.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <select
            name="company"
            defaultValue={searchParams?.company ?? ""}
            className="h-9 max-w-[160px] rounded-lg border border-[#333] bg-[#1a1a1a] px-3 text-sm text-white"
          >
            <option value="">Company</option>
            {companies.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          <button
            type="submit"
            className="h-9 rounded-lg bg-[#ffa116] px-4 text-sm font-semibold text-[#1a1a1a] hover:bg-[#ffb84d]"
          >
            Filter
          </button>
        </form>

        <ProblemListTable problems={problems} />
      </div>
    </div>
  );
}
