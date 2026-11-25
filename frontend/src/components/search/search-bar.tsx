"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

export function SearchBar({
  className,
  placeholder = "Search lessons, problems, courses…",
  size = "default",
}: {
  className?: string;
  placeholder?: string;
  size?: "default" | "lg";
}) {
  const router = useRouter();
  const [query, setQuery] = useState("");

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    const q = query.trim();
    if (!q) return;
    router.push(`/search?q=${encodeURIComponent(q)}`);
  }

  return (
    <form onSubmit={onSubmit} className={cn("relative w-full", className)} role="search">
      <Search
        className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
        aria-hidden
      />
      <Input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        aria-label="Search"
        className={cn(
          "pl-9",
          size === "lg" && "h-12 rounded-lg text-base shadow-sm",
        )}
      />
    </form>
  );
}
