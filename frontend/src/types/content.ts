export type Difficulty =
  | "beginner"
  | "intermediate"
  | "advanced"
  | "easy"
  | "medium"
  | "hard";

export interface LessonSummary {
  slug: string;
  title: string;
  summary: string;
  duration: number;
  difficulty: string;
  order: number;
  tags: string[];
  module: string;
  course: string;
}

export interface LessonDetail extends LessonSummary {
  prerequisites: string[];
  content: string;
  previous_slug: string | null;
  next_slug: string | null;
}

export interface ModuleSummary {
  slug: string;
  title: string;
  order: number;
  lessons: LessonSummary[];
}

export interface CourseSummary {
  slug: string;
  title: string;
  summary: string;
  category: string;
  difficulty: string;
  duration_hours: number;
  lesson_count: number;
  tags: string[];
  thumbnail: string | null;
}

export interface CourseDetail extends CourseSummary {
  prerequisites: string[];
  learning_outcomes: string[];
  modules: ModuleSummary[];
  description: string;
}

export interface ProblemSummary {
  slug: string;
  title: string;
  difficulty: string;
  topics: string[];
  company_tags: string[];
}

export interface ProblemExample {
  input: string;
  output: string;
  explanation?: string | null;
}

export interface ProblemTestCase {
  name: string;
  args: Record<string, unknown>;
  expected: unknown;
}

export interface ProblemDetail extends ProblemSummary {
  statement: string;
  constraints: string[];
  examples: ProblemExample[];
  starter_code: string;
  function_name?: string;
  hints: string[];
  editorial?: string | null;
  approaches: Array<Record<string, unknown>>;
  visible_tests?: ProblemTestCase[];
  /** Prefer server-side submit for hidden tests; optional for local tooling. */
  hidden_tests?: ProblemTestCase[];
}

export interface SearchHit {
  type: "lesson" | "problem" | "course";
  slug: string;
  title: string;
  summary: string;
  course?: string | null;
  difficulty?: string | null;
  score: number;
}

export interface LessonFrontmatter {
  title: string;
  slug: string;
  summary: string;
  duration: number;
  difficulty: string;
  prerequisites?: string[];
  tags?: string[];
  order: number;
}
