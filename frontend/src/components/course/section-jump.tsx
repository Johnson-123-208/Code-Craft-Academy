"use client";

import { useEffect, useState } from "react";

export function SectionJump({
  contentSelector = ".mdx-content",
}: {
  contentSelector?: string;
}) {
  const [sections, setSections] = useState<Array<{ id: string; text: string }>>(
    [],
  );

  useEffect(() => {
    const root = document.querySelector(contentSelector);
    if (!root) return;
    const nodes = Array.from(root.querySelectorAll("h2"));
    setSections(
      nodes
        .map((node) => ({
          id: node.id,
          text: (node.textContent ?? "").trim(),
        }))
        .filter((h) => h.id && h.text),
    );
  }, [contentSelector]);

  if (sections.length < 2) return null;

  return (
    <label className="mb-5 flex items-center gap-2 rounded-md border border-[#333] bg-[#262626] px-2.5 py-1.5">
      <span className="shrink-0 text-[10px] font-semibold uppercase tracking-wide text-[#eff1f666]">
        Jump
      </span>
      <select
        className="h-7 w-full rounded border-0 bg-transparent text-[13px] text-white outline-none"
        defaultValue=""
        onChange={(e) => {
          const id = e.target.value;
          if (!id) return;
          const el = document.getElementById(id);
          el?.scrollIntoView({ behavior: "smooth", block: "start" });
          e.currentTarget.value = "";
        }}
      >
        <option value="" disabled>
          Choose a section…
        </option>
        {sections.map((s) => (
          <option key={s.id} value={s.id}>
            {s.text}
          </option>
        ))}
      </select>
    </label>
  );
}
