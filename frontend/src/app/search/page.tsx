import Link from "next/link";
import { searchLocal } from "@/lib/search";
import { DifficultyText } from "@/components/leetcode/difficulty";

export const metadata = { title: "Search" };

function hrefFor(type: string, slug: string) {
  if (type === "course") return `/courses/${slug}`;
  if (type === "lesson") return `/lessons/${slug}`;
  return `/practice/${slug}`;
}

export default function SearchPage({
  searchParams,
}: {
  searchParams?: { q?: string };
}) {
  const q = searchParams?.q ?? "";
  const hits = q ? searchLocal(q) : [];

  return (
    <div className="min-h-[calc(100vh-3rem)] bg-[#1a1a1a] text-[#eff1f6]">
      <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
        <h1 className="text-2xl font-semibold text-white">Search</h1>
        <form className="mt-5" method="get">
          <input
            name="q"
            defaultValue={q}
            placeholder="Search problems, lessons, courses…"
            className="h-11 w-full rounded-xl border border-[#333] bg-[#262626] px-4 text-sm text-white placeholder:text-[#eff1f644] focus:border-[#ffa116] focus:outline-none"
          />
        </form>
        {q && (
          <p className="mt-4 text-sm text-[#eff1f666]">
            {hits.length} result{hits.length === 1 ? "" : "s"} for “{q}”
          </p>
        )}
        <ul className="mt-5 space-y-2">
          {hits.map((hit) => (
            <li key={`${hit.type}-${hit.slug}`}>
              <Link
                href={hrefFor(hit.type, hit.slug)}
                className="block rounded-xl border border-[#333] bg-[#262626] p-4 transition hover:border-[#ffa116]/50"
              >
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded bg-[#333] px-2 py-0.5 text-[11px] uppercase tracking-wide text-[#eff1f699]">
                    {hit.type}
                  </span>
                  {hit.difficulty && (
                    <DifficultyText difficulty={hit.difficulty} />
                  )}
                </div>
                <h2 className="mt-2 font-semibold text-white">{hit.title}</h2>
                <p className="mt-1 text-sm text-[#eff1f666]">{hit.summary}</p>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
