"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, Search, X } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/practice", label: "Problem List" },
  { href: "/catalog", label: "Explore" },
  { href: "/playground", label: "Playground" },
  { href: "/courses/dsa", label: "Interview" },
];

export function SiteHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const hideChrome =
    /^\/practice\/[^/]+$/.test(pathname) || pathname.startsWith("/lessons/");

  if (hideChrome) {
    return null;
  }

  return (
    <header className="sticky top-0 z-50 border-b border-[#333] bg-[#282828]">
      <div className="mx-auto flex h-12 max-w-[1400px] items-center gap-1 px-3 sm:px-4">
        <Link href="/" className="mr-3 flex items-center gap-2 pr-2">
          <span className="flex h-7 w-7 items-center justify-center rounded bg-[#ffa116] text-sm font-black text-[#1a1a1a]">
            C
          </span>
          <span className="hidden text-[15px] font-semibold tracking-tight text-[#eff1f6] sm:inline">
            CodeCraft
          </span>
        </Link>

        <nav className="hidden items-center md:flex" aria-label="Primary">
          {NAV.map((item) => {
            const active =
              item.href === "/practice"
                ? pathname.startsWith("/practice")
                : pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative px-3 py-3 text-sm transition-colors",
                  active
                    ? "font-medium text-white after:absolute after:inset-x-3 after:bottom-0 after:h-0.5 after:bg-[#ffa116]"
                    : "text-[#eff1f6aa] hover:text-white",
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="ml-auto flex items-center gap-2">
          <Link
            href="/search"
            className="inline-flex h-8 items-center gap-2 rounded-lg border border-[#3e3e3e] bg-[#1a1a1a] px-3 text-xs text-[#eff1f699] hover:border-[#555] hover:text-white"
          >
            <Search className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Search</span>
          </Link>
          <Link
            href="/practice"
            className="hidden h-8 items-center rounded-lg bg-[#ffa116] px-3 text-xs font-semibold text-[#1a1a1a] hover:bg-[#ffb84d] sm:inline-flex"
          >
            Start Coding
          </Link>
          <button
            type="button"
            className="inline-flex h-8 w-8 items-center justify-center rounded-lg text-[#eff1f6] hover:bg-[#333] md:hidden"
            aria-label={open ? "Close menu" : "Open menu"}
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {open && (
        <div className="border-t border-[#333] bg-[#262626] px-3 py-3 md:hidden">
          <nav className="flex flex-col" aria-label="Mobile">
            {NAV.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="rounded-md px-3 py-2.5 text-sm text-[#eff1f6] hover:bg-[#333]"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
}
