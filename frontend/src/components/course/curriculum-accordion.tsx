import Link from "next/link";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import type { ModuleSummary } from "@/types/content";
import { formatDuration } from "@/lib/utils";

export function CurriculumAccordion({ modules }: { modules: ModuleSummary[] }) {
  const defaultValue = modules[0] ? [modules[0].slug] : [];

  return (
    <Accordion type="multiple" defaultValue={defaultValue} className="w-full">
      {modules.map((module) => (
        <AccordionItem key={module.slug} value={module.slug}>
          <AccordionTrigger className="text-sm text-white hover:no-underline">
            <span>
              <span className="text-[#eff1f666]">Module {module.order} · </span>
              {module.title}
              <span className="ml-2 text-xs font-normal text-[#eff1f644]">
                ({module.lessons.length})
              </span>
            </span>
          </AccordionTrigger>
          <AccordionContent>
            <ul className="space-y-0.5">
              {module.lessons.map((lesson, idx) => (
                <li key={lesson.slug}>
                  <Link
                    href={`/lessons/${lesson.slug}`}
                    className="flex items-center justify-between rounded-md px-3 py-2 text-sm text-[#eff1f6bb] hover:bg-[#333] hover:text-[#ffa116]"
                  >
                    <span>
                      <span className="mr-2 text-[#eff1f644]">{idx + 1}.</span>
                      {lesson.title}
                    </span>
                    <span className="text-xs text-[#eff1f644]">
                      {formatDuration(lesson.duration)}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  );
}
