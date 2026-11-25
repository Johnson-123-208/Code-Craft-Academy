"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

interface Heading {
  id: string;
  text: string;
  level: number;
}

export function TableOfContents({ contentSelector = ".mdx-content" }: { contentSelector?: string }) {
  const [headings, setHeadings] = useState<Heading[]>([]);
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    const root = document.querySelector(contentSelector);
    if (!root) return;
    const nodes = Array.from(root.querySelectorAll("h2, h3"));
    const parsed = nodes.map((node) => ({
      id: node.id,
      text: node.textContent ?? "",
      level: node.tagName === "H2" ? 2 : 3,
    }));
    setHeadings(parsed.filter((h) => h.id));

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]?.target.id) setActiveId(visible[0].target.id);
      },
      { rootMargin: "-20% 0px -70% 0px", threshold: [0, 1] },
    );

    nodes.forEach((n) => observer.observe(n));
    return () => observer.disconnect();
  }, [contentSelector]);

  if (headings.length === 0) return null;

  return (
    <nav aria-label="On this page" className="sticky top-24">
      <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-[#eff1f666]">
        On this page
      </p>
      <ul className="space-y-1 border-l border-[#333] text-sm">
        {headings.map((heading) => (
          <li key={heading.id}>
            <a
              href={`#${heading.id}`}
              className={cn(
                "block border-l-2 border-transparent py-1 text-[#eff1f666] transition hover:text-white",
                heading.level === 3 && "pl-4",
                heading.level === 2 && "pl-3",
                activeId === heading.id &&
                  "border-[#ffa116] font-medium text-[#ffa116]",
              )}
            >
              {heading.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
