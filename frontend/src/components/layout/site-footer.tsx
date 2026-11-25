"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function SiteFooter() {
  const pathname = usePathname();
  if (
    /^\/practice\/[^/]+$/.test(pathname) ||
    pathname === "/playground" ||
    pathname.startsWith("/lessons/")
  ) {
    return null;
  }

  return (
    <footer className="border-t border-[#333] bg-[#1a1a1a]">
      <div className="mx-auto flex max-w-[1400px] flex-col gap-6 px-4 py-10 sm:flex-row sm:justify-between sm:px-6">
        <div>
          <p className="flex items-center gap-2 text-sm font-semibold text-white">
            <span className="flex h-6 w-6 items-center justify-center rounded bg-[#ffa116] text-xs font-black text-[#1a1a1a]">
              C
            </span>
            CodeCraft Academy
          </p>
          <p className="mt-2 max-w-sm text-xs leading-5 text-[#eff1f666]">
            LeetCode-style practice + textbook courses for Python, DSA, System
            Design, Cloud, and AI/ML.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-8 text-xs sm:grid-cols-3">
          <div className="space-y-2">
            <p className="font-semibold text-[#eff1f6aa]">Practice</p>
            <Link className="block text-[#eff1f666] hover:text-[#ffa116]" href="/practice">
              Problem List
            </Link>
            <Link className="block text-[#eff1f666] hover:text-[#ffa116]" href="/playground">
              Playground
            </Link>
          </div>
          <div className="space-y-2">
            <p className="font-semibold text-[#eff1f6aa]">Learn</p>
            <Link className="block text-[#eff1f666] hover:text-[#ffa116]" href="/catalog">
              Explore
            </Link>
            <Link className="block text-[#eff1f666] hover:text-[#ffa116]" href="/courses/dsa">
              DSA
            </Link>
            <Link className="block text-[#eff1f666] hover:text-[#ffa116]" href="/courses/python">
              Python
            </Link>
          </div>
          <div className="space-y-2">
            <p className="font-semibold text-[#eff1f6aa]">More</p>
            <Link className="block text-[#eff1f666] hover:text-[#ffa116]" href="/courses/system-design">
              System Design
            </Link>
            <Link className="block text-[#eff1f666] hover:text-[#ffa116]" href="/courses/ai-ml">
              AI / ML
            </Link>
          </div>
        </div>
      </div>
      <div className="border-t border-[#333] px-4 py-3 text-center text-[11px] text-[#eff1f666]">
        © {new Date().getFullYear()} CodeCraft Academy · Built by{" "}
        <span className="font-medium text-[#eff1f6aa]">Johnson Obhalloju</span>
      </div>
    </footer>
  );
}
