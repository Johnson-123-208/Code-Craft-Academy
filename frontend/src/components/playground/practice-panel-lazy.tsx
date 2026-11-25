"use client";

import dynamic from "next/dynamic";

export const PracticePanelLazy = dynamic(
  () =>
    import("@/components/playground/practice-panel").then(
      (m) => m.PracticePanel,
    ),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-full min-h-[320px] flex-col bg-[#1a1a1a]">
        <div className="flex h-10 items-center border-b border-[#333] bg-[#262626] px-3 text-xs text-[#eff1f666]">
          Loading editor…
        </div>
        <div className="flex flex-1 items-center justify-center text-xs text-[#eff1f666]">
          Preparing Monaco…
        </div>
      </div>
    ),
  },
);
