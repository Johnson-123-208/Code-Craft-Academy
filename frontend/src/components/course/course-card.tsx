import Link from "next/link";
import { BookOpen, Clock } from "lucide-react";
import { DifficultyText } from "@/components/leetcode/difficulty";
import type { CourseSummary } from "@/types/content";

export function CourseCard({ course }: { course: CourseSummary }) {
  return (
    <Link
      href={`/courses/${course.slug}`}
      className="group flex flex-col overflow-hidden rounded-xl border border-[#333] bg-[#262626] transition hover:border-[#ffa116]/50"
    >
      <div className="relative aspect-[16/9] overflow-hidden bg-[#1a1a1a]">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={course.thumbnail ?? "/images/courses/python.svg"}
          alt=""
          className="h-full w-full object-cover opacity-80 transition duration-500 group-hover:scale-105"
        />
        <span className="absolute bottom-3 left-3 text-[11px] font-semibold uppercase tracking-wider text-white/90">
          {course.category}
        </span>
      </div>
      <div className="flex flex-1 flex-col gap-3 p-4">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-[15px] font-semibold leading-snug text-white group-hover:text-[#ffa116]">
            {course.title}
          </h3>
          <DifficultyText difficulty={course.difficulty} />
        </div>
        <p className="line-clamp-3 text-xs leading-5 text-[#eff1f666]">
          {course.summary}
        </p>
        <div className="mt-auto flex items-center gap-4 pt-1 text-[11px] text-[#eff1f644]">
          <span className="inline-flex items-center gap-1">
            <Clock className="h-3 w-3" aria-hidden />
            {course.duration_hours > 0 ? `${course.duration_hours}h` : "Growing"}
          </span>
          <span className="inline-flex items-center gap-1">
            <BookOpen className="h-3 w-3" aria-hidden />
            {course.lesson_count} lessons
          </span>
        </div>
      </div>
    </Link>
  );
}
