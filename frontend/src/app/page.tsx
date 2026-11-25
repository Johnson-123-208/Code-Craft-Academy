import Link from "next/link";
import { ArrowRight, Code2, BookOpen, Terminal } from "lucide-react";
import { ProblemListTable } from "@/components/leetcode/problem-list";
import { listCourses, listProblems } from "@/lib/content";

export default function HomePage() {
  const problems = listProblems().slice(0, 12);
  const courses = listCourses();

  return (
    <div className="bg-[#1a1a1a] text-[#eff1f6]">
      <section className="border-b border-[#333] bg-[#262626]">
        <div className="mx-auto flex max-w-[1400px] flex-col gap-8 px-4 py-14 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="max-w-xl">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#ffa116]">
              CodeCraft Academy
            </p>
            <h1 className="mt-3 text-4xl font-semibold tracking-tight text-white sm:text-5xl">
              A LeetCode-style path to job-ready engineering
            </h1>
            <p className="mt-4 text-[15px] leading-7 text-[#eff1f699]">
              Solve problems in a familiar workspace. Study textbook-depth
              courses for Python, DSA, System Design, Cloud, and AI/ML — with a
              live Python runner.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link
                href="/practice"
                className="inline-flex h-10 items-center gap-2 rounded-lg bg-[#ffa116] px-4 text-sm font-semibold text-[#1a1a1a] hover:bg-[#ffb84d]"
              >
                <Code2 className="h-4 w-4" />
                Problem List
              </Link>
              <Link
                href="/catalog"
                className="inline-flex h-10 items-center gap-2 rounded-lg border border-[#444] bg-transparent px-4 text-sm font-medium text-white hover:bg-[#333]"
              >
                Explore courses
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>

          <div className="grid w-full max-w-md grid-cols-3 gap-3">
            {[
              { label: "Problems", value: String(listProblems().length), href: "/practice" },
              { label: "Courses", value: String(courses.length), href: "/catalog" },
              { label: "Playground", value: "Python", href: "/playground" },
            ].map((stat) => (
              <Link
                key={stat.label}
                href={stat.href}
                className="rounded-xl border border-[#333] bg-[#1a1a1a] p-4 text-center hover:border-[#ffa116]/50"
              >
                <p className="text-2xl font-semibold text-white">{stat.value}</p>
                <p className="mt-1 text-[11px] uppercase tracking-wide text-[#eff1f666]">
                  {stat.label}
                </p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-[1400px] px-4 py-10 sm:px-6">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Featured problems</h2>
          <Link href="/practice" className="text-sm text-[#ffa116] hover:underline">
            View all
          </Link>
        </div>
        <ProblemListTable problems={problems} />
      </section>

      <section className="border-t border-[#333] bg-[#1f1f1f]">
        <div className="mx-auto max-w-[1400px] px-4 py-10 sm:px-6">
          <h2 className="text-lg font-semibold text-white">Study plans</h2>
          <p className="mt-1 text-sm text-[#eff1f699]">
            Structured courses that pair with the problemset.
          </p>
          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
            {courses.map((course) => (
              <Link
                key={course.slug}
                href={`/courses/${course.slug}`}
                className="group rounded-xl border border-[#333] bg-[#262626] p-4 transition hover:border-[#ffa116]/60"
              >
                <BookOpen className="h-5 w-5 text-[#ffa116]" />
                <h3 className="mt-3 text-sm font-semibold text-white group-hover:text-[#ffa116]">
                  {course.title}
                </h3>
                <p className="mt-2 line-clamp-3 text-xs leading-5 text-[#eff1f666]">
                  {course.summary}
                </p>
                <p className="mt-3 text-[11px] text-[#eff1f644]">
                  {course.lesson_count} lessons
                </p>
              </Link>
            ))}
          </div>
          <Link
            href="/playground"
            className="mt-6 inline-flex items-center gap-2 text-sm text-[#eff1f699] hover:text-[#ffa116]"
          >
            <Terminal className="h-4 w-4" />
            Open Python Playground
          </Link>
        </div>
      </section>
    </div>
  );
}
