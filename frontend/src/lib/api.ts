import type {
  CourseDetail,
  CourseSummary,
  LessonDetail,
  ProblemDetail,
  ProblemSummary,
  SearchHit,
} from "@/types/content";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      Accept: "application/json",
      ...(init?.headers ?? {}),
    },
    next: { revalidate: 60 },
  });
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export function getCourses(): Promise<CourseSummary[]> {
  return apiGet("/api/courses");
}

export function getCourse(slug: string): Promise<CourseDetail> {
  return apiGet(`/api/courses/${slug}`);
}

export function getLesson(slug: string): Promise<LessonDetail> {
  return apiGet(`/api/lessons/${slug}`);
}

export function getProblems(params?: {
  topic?: string;
  difficulty?: string;
  company?: string;
}): Promise<ProblemSummary[]> {
  const qs = new URLSearchParams();
  if (params?.topic) qs.set("topic", params.topic);
  if (params?.difficulty) qs.set("difficulty", params.difficulty);
  if (params?.company) qs.set("company", params.company);
  const suffix = qs.toString() ? `?${qs}` : "";
  return apiGet(`/api/problems${suffix}`);
}

export function getProblem(slug: string): Promise<ProblemDetail> {
  return apiGet(`/api/problems/${slug}`);
}

export async function searchContent(query: string): Promise<SearchHit[]> {
  const data = await apiGet<{ hits: SearchHit[] }>(
    `/api/search?q=${encodeURIComponent(query)}`,
  );
  return data.hits;
}

export async function runCode(code: string, stdin = "") {
  const res = await fetch(`${API_URL}/api/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, stdin, language: "python" }),
  });
  return res.json();
}

export async function submitCode(problemSlug: string, code: string) {
  const res = await fetch(`${API_URL}/api/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      problem_slug: problemSlug,
      code,
      language: "python",
    }),
  });
  return res.json();
}
