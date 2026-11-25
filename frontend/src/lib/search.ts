import Fuse from "fuse.js";
import { buildSearchIndex } from "@/lib/content";
import type { SearchHit } from "@/types/content";

let fuse: Fuse<SearchHit> | null = null;

function getFuse(): Fuse<SearchHit> {
  if (!fuse) {
    fuse = new Fuse(buildSearchIndex(), {
      keys: [
        { name: "title", weight: 0.5 },
        { name: "summary", weight: 0.3 },
        { name: "course", weight: 0.1 },
        { name: "difficulty", weight: 0.1 },
      ],
      threshold: 0.35,
      includeScore: true,
    });
  }
  return fuse;
}

export function searchLocal(query: string, limit = 20): SearchHit[] {
  const q = query.trim();
  if (!q) return [];
  return getFuse()
    .search(q, { limit })
    .map((result) => ({
      ...result.item,
      score: result.score != null ? 1 - result.score : 0,
    }));
}
