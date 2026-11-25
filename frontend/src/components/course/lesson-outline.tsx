"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { ChevronDown } from "lucide-react";
import type { CourseDetail } from "@/types/content";
import { cn } from "@/lib/utils";

export function LessonOutline({
  course,
  currentSlug,
}: {
  course: CourseDetail;
  currentSlug: string;
}) {
  const currentModule = useMemo(
    () =>
      course.modules.find((m) =>
        m.lessons.some((l) => l.slug === currentSlug),
      )?.slug ?? course.modules[0]?.slug,
    [course.modules, currentSlug],
  );

  const [openModules, setOpenModules] = useState<Record<string, boolean>>(
    () =>
      Object.fromEntries(
        course.modules.map((m) => [m.slug, m.slug === currentModule]),
      ),
  );

  function toggle(slug: string) {
    setOpenModules((prev) => ({ ...prev, [slug]: !prev[slug] }));
  }

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="shrink-0 border-b border-[#333] px-3 py-2">
        <p className="line-clamp-2 text-[12px] font-medium leading-snug text-white">
          {course.title}
        </p>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-1.5 py-1.5">
        {course.modules.map((module) => {
          const open = openModules[module.slug] ?? false;
          return (
            <div key={module.slug} className="mb-1">
              <button
                type="button"
                onClick={() => toggle(module.slug)}
                className="flex w-full items-center gap-2 rounded-md px-2 py-2 text-left text-[13px] font-semibold text-[#eff1f6cc] hover:bg-[#2a2a2a]"
              >
                <ChevronDown
                  className={cn(
                    "h-3.5 w-3.5 shrink-0 text-[#eff1f666] transition",
                    !open && "-rotate-90",
                  )}
                />
                <span className="min-w-0 flex-1 leading-snug">
                  {module.title}
                </span>
                <span className="text-[11px] font-normal text-[#eff1f655]">
                  {module.lessons.length}
                </span>
              </button>

              {open && (
                <ul className="mb-2 ml-2 space-y-0.5 border-l border-[#333] pl-2">
                  {module.lessons.map((lesson) => {
                    const active = lesson.slug === currentSlug;
                    return (
                      <li key={lesson.slug}>
                        <Link
                          href={`/lessons/${lesson.slug}`}
                          className={cn(
                            "block rounded-md px-2.5 py-2 text-[13px] leading-snug transition",
                            active
                              ? "bg-[#2a2a2a] font-medium text-[#ffa116]"
                              : "text-[#eff1f699] hover:bg-[#2a2a2a] hover:text-white",
                          )}
                        >
                          {lesson.title}
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
