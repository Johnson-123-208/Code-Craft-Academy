import Link from "next/link";
import { notFound } from "next/navigation";
import { CheckCircle2, Clock, Layers } from "lucide-react";
import { CurriculumAccordion } from "@/components/course/curriculum-accordion";
import { DifficultyText } from "@/components/leetcode/difficulty";
import { getCourse, listCourses } from "@/lib/content";

export function generateStaticParams() {
  return listCourses().map((c) => ({ slug: c.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }) {
  const course = getCourse(params.slug);
  if (!course) return { title: "Course" };
  return { title: course.title, description: course.summary };
}

export default function CoursePage({ params }: { params: { slug: string } }) {
  const course = getCourse(params.slug);
  if (!course) notFound();
  const firstLesson = course.modules[0]?.lessons[0];

  return (
    <div className="bg-[#1a1a1a] text-[#eff1f6]">
      <section className="border-b border-[#333] bg-[#262626]">
        <div className="mx-auto max-w-[1400px] px-4 py-12 sm:px-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#ffa116]">
            {course.category}
          </p>
          <h1 className="mt-2 max-w-3xl text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            {course.title}
          </h1>
          <p className="mt-3 max-w-2xl text-[15px] leading-7 text-[#eff1f699]">
            {course.summary}
          </p>
          <div className="mt-5 flex flex-wrap items-center gap-4 text-sm text-[#eff1f666]">
            <DifficultyText difficulty={course.difficulty} />
            <span className="inline-flex items-center gap-1">
              <Clock className="h-4 w-4" /> {course.duration_hours}h
            </span>
            <span className="inline-flex items-center gap-1">
              <Layers className="h-4 w-4" /> {course.lesson_count} lessons
            </span>
          </div>
          {firstLesson && (
            <Link
              href={`/lessons/${firstLesson.slug}`}
              className="mt-7 inline-flex h-10 items-center rounded-lg bg-[#ffa116] px-5 text-sm font-semibold text-[#1a1a1a] hover:bg-[#ffb84d]"
            >
              Start learning
            </Link>
          )}
        </div>
      </section>

      <div className="mx-auto grid max-w-[1400px] gap-8 px-4 py-10 lg:grid-cols-[1fr_300px] sm:px-6">
        <div>
          <h2 className="text-lg font-semibold text-white">Overview</h2>
          <p className="mt-3 text-sm leading-7 text-[#eff1f699]">{course.description}</p>

          <h2 className="mt-10 text-lg font-semibold text-white">What you&apos;ll learn</h2>
          <ul className="mt-4 space-y-3">
            {course.learning_outcomes.map((item) => (
              <li key={item} className="flex gap-3 text-sm leading-6 text-[#eff1f6bb]">
                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-[#2cbb5d]" />
                {item}
              </li>
            ))}
          </ul>

          <h2 className="mt-10 text-lg font-semibold text-white">Curriculum</h2>
          <div className="mt-4 rounded-xl border border-[#333] bg-[#262626] px-4">
            <CurriculumAccordion modules={course.modules} />
          </div>
        </div>

        <aside className="h-fit rounded-xl border border-[#333] bg-[#262626] p-5 lg:sticky lg:top-16">
          <h3 className="font-semibold text-white">Prerequisites</h3>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-[#eff1f699]">
            {course.prerequisites.map((p) => (
              <li key={p}>{p}</li>
            ))}
          </ul>
          <div className="mt-5 flex flex-wrap gap-2">
            {course.tags.map((tag) => (
              <span
                key={tag}
                className="rounded-full bg-[#333] px-2.5 py-0.5 text-xs text-[#eff1f6aa]"
              >
                {tag}
              </span>
            ))}
          </div>
        </aside>
      </div>
    </div>
  );
}
