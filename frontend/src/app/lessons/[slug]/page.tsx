import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft, ChevronRight, Clock } from "lucide-react";
import { LessonOutline } from "@/components/course/lesson-outline";
import { LessonWorkspace } from "@/components/course/lesson-workspace";
import { SectionJump } from "@/components/course/section-jump";
import { MdxContent } from "@/components/mdx/mdx-content";
import { PracticePanelLazy } from "@/components/playground/practice-panel-lazy";
import { DifficultyText } from "@/components/leetcode/difficulty";
import { getCourse, getLesson, listLessonSlugs } from "@/lib/content";
import { formatDuration } from "@/lib/utils";

export function generateStaticParams() {
  return listLessonSlugs().map((slug) => ({ slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }) {
  const lesson = getLesson(params.slug);
  if (!lesson) return { title: "Lesson" };
  return { title: lesson.title, description: lesson.summary };
}

export default async function LessonPage({
  params,
}: {
  params: { slug: string };
}) {
  const lesson = getLesson(params.slug);
  if (!lesson) notFound();
  const course = getCourse(lesson.course);
  if (!course) notFound();

  const pythonBlocks = [
    ...lesson.content.matchAll(/```python\n([\s\S]*?)```/g),
  ].map((m) => m[1]?.trim() ?? "");
  const starter =
    pythonBlocks.find(
      (b) =>
        b.length > 40 &&
        !b.includes("input(") &&
        (b.includes("def ") || b.includes("print(") || b.includes("import ")),
    ) ||
    pythonBlocks.find((b) => b.includes("def ") || b.includes("print(")) ||
    undefined;

  return (
    <LessonWorkspace
      breadcrumb={
        <>
          <Link href="/catalog" className="hover:text-[#ffa116]">
            Explore
          </Link>
          <span className="mx-1.5 text-[#eff1f644]">/</span>
          <Link
            href={`/courses/${course.slug}`}
            className="hover:text-[#ffa116]"
          >
            {course.title}
          </Link>
          <span className="mx-1.5 text-[#eff1f644]">/</span>
          <span className="text-[#eff1f6aa]">{lesson.title}</span>
        </>
      }
      outline={<LessonOutline course={course} currentSlug={lesson.slug} />}
      practice={<PracticePanelLazy initialCode={starter} />}
      content={
        <>
          <header className="mb-5 border-b border-[#333] pb-4">
            <div className="flex flex-wrap items-center gap-2.5">
              <DifficultyText difficulty={lesson.difficulty} />
              <span className="inline-flex items-center gap-1 text-[11px] text-[#eff1f666]">
                <Clock className="h-3 w-3" />
                {formatDuration(lesson.duration)}
              </span>
            </div>
            <h1 className="mt-2 text-[1.5rem] font-semibold leading-snug tracking-tight text-white sm:text-[1.75rem]">
              {lesson.title}
            </h1>
            <p className="mt-2 text-[14px] leading-6 text-[#b8bec9]">
              {lesson.summary}
            </p>
          </header>

          <SectionJump />

          <div className="lc-prose mdx-content">
            <MdxContent source={lesson.content} />
          </div>

          <nav className="mt-10 flex items-center justify-between gap-3 border-t border-[#333] pt-5 pb-2">
            {lesson.previous_slug ? (
              <Link
                href={`/lessons/${lesson.previous_slug}`}
                className="inline-flex max-w-[45%] items-center gap-1.5 rounded-md border border-[#333] bg-[#262626] px-2.5 py-2 text-xs text-[#eff1f6aa] hover:border-[#ffa116]/50 hover:text-[#ffa116]"
              >
                <ChevronLeft className="h-3.5 w-3.5 shrink-0" />
                <span className="truncate">Previous</span>
              </Link>
            ) : (
              <span />
            )}
            {lesson.next_slug ? (
              <Link
                href={`/lessons/${lesson.next_slug}`}
                className="inline-flex max-w-[45%] items-center gap-1.5 rounded-md border border-[#333] bg-[#262626] px-2.5 py-2 text-xs text-[#eff1f6aa] hover:border-[#ffa116]/50 hover:text-[#ffa116]"
              >
                <span className="truncate">Next lesson</span>
                <ChevronRight className="h-3.5 w-3.5 shrink-0" />
              </Link>
            ) : (
              <span />
            )}
          </nav>
        </>
      }
    />
  );
}
