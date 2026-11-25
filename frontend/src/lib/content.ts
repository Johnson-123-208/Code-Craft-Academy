import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import type {
  CourseDetail,
  CourseSummary,
  LessonDetail,
  LessonSummary,
  ModuleSummary,
  ProblemDetail,
  ProblemSummary,
  SearchHit,
} from "@/types/content";

const COURSE_META: Record<
  string,
  Omit<CourseDetail, "duration_hours" | "lesson_count" | "modules"> & {
    duration_hours?: number;
    lesson_count?: number;
  }
> = {
  python: {
    slug: "python",
    title: "Python from Zero to Advanced",
    summary:
      "A complete Python curriculum from first REPL session to packaging, concurrency, testing, and production APIs.",
    category: "Programming",
    difficulty: "beginner",
    tags: ["python", "oop", "asyncio", "testing"],
    thumbnail: "/images/courses/python.svg",
    prerequisites: ["None — start from absolute zero"],
    learning_outcomes: [
      "Write idiomatic, production-quality Python",
      "Master OOP, generators, decorators, and concurrency",
      "Test, package, and ship Python applications",
    ],
    description:
      "This course takes you from installing Python to writing clean, typed, tested code. Every lesson pairs deep explanation with runnable examples you can edit in the in-browser playground.",
  },
  dsa: {
    slug: "dsa",
    title: "Data Structures and Algorithms",
    summary:
      "Master Big-O, classic data structures, and problem-solving patterns with dry-runs, diagrams, and hundreds of practice problems.",
    category: "Algorithms",
    difficulty: "intermediate",
    tags: ["dsa", "algorithms", "interview", "big-o"],
    thumbnail: "/images/courses/dsa.svg",
    prerequisites: ["Comfortable with basic Python syntax"],
    learning_outcomes: [
      "Analyze time and space complexity rigorously",
      "Implement and apply core data structures",
      "Recognize and apply the major problem-solving patterns",
    ],
    description:
      "A mastery track for interviews and real engineering: arrays to graphs, DP frameworks, string algorithms, and a pattern cheat sheet.",
  },
  "system-design": {
    slug: "system-design",
    title: "System Design and Software Architecture",
    summary:
      "Scalability, building blocks, architecture styles, and full case studies from URL shorteners to ML inference platforms.",
    category: "Architecture",
    difficulty: "advanced",
    tags: ["system-design", "distributed-systems", "architecture"],
    thumbnail: "/images/courses/system-design.svg",
    prerequisites: ["1+ years of backend experience recommended"],
    learning_outcomes: [
      "Estimate capacity and choose the right building blocks",
      "Design for availability, consistency, and latency trade-offs",
      "Produce interview-ready architecture diagrams and designs",
    ],
    description:
      "From CAP and PACELC to Kafka, caching, and end-to-end case studies with Mermaid architecture diagrams.",
  },
  "cloud-devops": {
    slug: "cloud-devops",
    title: "Cloud, DevOps, CI/CD and Deployment",
    summary:
      "AWS core services, Terraform, Docker, Kubernetes, CI/CD pipelines, observability, and hands-on deployment of this very platform.",
    category: "Cloud & DevOps",
    difficulty: "intermediate",
    tags: ["aws", "docker", "kubernetes", "terraform", "cicd"],
    thumbnail: "/images/courses/cloud-devops.svg",
    prerequisites: ["Basic Linux and networking familiarity"],
    learning_outcomes: [
      "Provision and operate workloads on AWS",
      "Containerize apps and orchestrate with Kubernetes",
      "Build secure CI/CD pipelines and monitor production",
    ],
    description:
      "A practical DevOps path covering cloud fundamentals through GitOps, with architecture diagrams for deploying CodeCraft Academy.",
  },
  "ai-ml": {
    slug: "ai-ml",
    title: "AI / ML / Data Science",
    summary:
      "Math foundations, classical ML from scratch, deep learning, NLP/LLMs, MLOps, and AWS SageMaker end to end.",
    category: "AI & Machine Learning",
    difficulty: "advanced",
    tags: ["machine-learning", "deep-learning", "sagemaker", "nlp"],
    thumbnail: "/images/courses/ai-ml.svg",
    prerequisites: ["Python fluency", "High-school math (refreshers included)"],
    learning_outcomes: [
      "Derive and implement core ML algorithms from scratch",
      "Train, evaluate, and serve models with modern tooling",
      "Operate ML systems with MLOps and SageMaker",
    ],
    description:
      "Deep coverage from linear algebra intuition to Transformers, RAG, and production SageMaker pipelines — all with runnable Python.",
  },
};

const MODULE_TITLES: Record<string, string> = {
  "01-getting-started": "Getting Started",
  "01-foundations": "Foundations: Complexity and Approach",
  "02-arrays-strings": "Arrays and Strings",
  "03-hashing": "Hashing",
  "04-linked-lists": "Linked Lists",
  "05-stacks-queues": "Stacks and Queues",
  "06-recursion-backtracking": "Recursion and Backtracking",
  "07-searching-sorting": "Searching and Sorting",
  "08-trees": "Trees",
  "09-heaps": "Heaps",
  "10-graphs": "Graphs",
  "11-dp": "Dynamic Programming",
  "12-greedy": "Greedy Algorithms",
  "13-bit-manipulation": "Bit Manipulation",
  "14-math-number-theory": "Math and Number Theory",
  "15-string-algorithms": "String Algorithms",
  "16-advanced": "Advanced Techniques",
  "17-patterns-interview": "Patterns and Interview Strategy",
  "01-fundamentals": "Fundamentals",
  "02-building-blocks": "Building Blocks",
  "03-architecture-styles": "Architecture Styles",
  "04-communication": "Communication",
  "05-reliability": "Reliability",
  "06-security": "Security",
  "07-case-studies": "Case Studies",
  "08-lld": "Low-Level Design",
  "01-cloud-fundamentals": "Cloud Fundamentals",
  "02-aws-core": "AWS Core Services",
  "03-terraform": "Terraform",
  "04-docker": "Docker",
  "05-kubernetes": "Kubernetes",
  "06-cicd": "CI/CD",
  "07-linux-networking": "Linux and Networking",
  "08-monitoring-cost": "Monitoring and Cost",
  "09-deploy-codecraft": "Deploy CodeCraft",
  "01-math-foundations": "Math Foundations",
  "02-python-data": "Python for Data",
  "03-ml-fundamentals": "ML Fundamentals",
  "04-classical-ml": "Classical Machine Learning",
  "05-deep-learning": "Deep Learning",
  "06-nlp-llms": "NLP and Large Language Models",
  "07-cv-timeseries-xai": "Vision, Time Series, and Explainability",
  "08-mlops": "MLOps",
  "09-sagemaker": "AWS SageMaker",
  "10-capstones": "Capstone Projects",
  "02-syntax-and-types": "Syntax and Types",
  "03-control-flow": "Control Flow",
  "04-functions": "Functions",
  "05-data-structures": "Data Structures",
  "06-strings-files": "Strings and Files",
  "07-errors-logging": "Errors and Logging",
  "08-oop": "Object-Oriented Programming",
  "09-modules-packages": "Modules and Packages",
  "10-itertools-functools": "Itertools and Functools",
  "11-typing": "Typing",
  "12-concurrency": "Concurrency",
  "13-testing": "Testing",
  "14-performance": "Performance",
  "15-web-apis": "Web APIs",
  "16-databases": "Databases",
  "17-packaging-quality": "Packaging and Quality",
};

export function getContentRoot(): string {
  if (process.env.CONTENT_DIR) return process.env.CONTENT_DIR;
  // repo_root/content — works in local next dev and Docker when mounted
  return path.resolve(process.cwd(), "..", "content");
}

type ParsedLesson = LessonSummary & {
  content: string;
  prerequisites: string[];
};

type ContentIndex = {
  root: string;
  builtAt: number;
  bySlug: Map<string, ParsedLesson>;
  byCourse: Map<string, ParsedLesson[]>;
  courses: CourseSummary[];
  courseDetails: Map<string, CourseDetail>;
  problems: ProblemSummary[];
  problemsBySlug: Map<string, ProblemDetail>;
};

const CACHE_TTL_MS = process.env.NODE_ENV === "development" ? 3_000 : 60_000;
let contentIndex: ContentIndex | null = null;

function parseLessonFile(
  filePath: string,
  course: string,
  moduleSlug: string,
): ParsedLesson {
  const raw = fs.readFileSync(filePath, "utf8");
  const { data, content } = matter(raw);
  const slug =
    (data.slug as string) ||
    path.basename(filePath).replace(/\.mdx?$/, "");
  return {
    slug,
    title: String(data.title ?? slug),
    summary: String(data.summary ?? ""),
    duration: Number(data.duration ?? 15),
    difficulty: String(data.difficulty ?? "beginner"),
    order: Number(data.order ?? 0),
    tags: Array.isArray(data.tags) ? data.tags.map(String) : [],
    module: moduleSlug,
    course,
    content,
    prerequisites: Array.isArray(data.prerequisites)
      ? data.prerequisites.map(String)
      : [],
  };
}

function iterLessonFiles(course?: string) {
  const root = getContentRoot();
  const courses = course ? [course] : Object.keys(COURSE_META);
  const results: Array<{ course: string; module: string; filePath: string }> =
    [];

  for (const c of courses) {
    const courseDir = path.join(root, c);
    if (!fs.existsSync(courseDir)) continue;
    const modules = fs
      .readdirSync(courseDir, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name)
      .sort();
    for (const moduleSlug of modules) {
      const moduleDir = path.join(courseDir, moduleSlug);
      const files = fs
        .readdirSync(moduleDir)
        .filter((f) => f.endsWith(".mdx"))
        .sort();
      for (const file of files) {
        results.push({
          course: c,
          module: moduleSlug,
          filePath: path.join(moduleDir, file),
        });
      }
    }
  }
  return results;
}

function toLessonSummary(lesson: ParsedLesson): LessonSummary {
  const { content: _c, prerequisites: _p, ...summary } = lesson;
  return summary;
}

function buildContentIndex(): ContentIndex {
  const root = getContentRoot();
  const bySlug = new Map<string, ParsedLesson>();
  const byCourse = new Map<string, ParsedLesson[]>();

  for (const { course, module, filePath } of iterLessonFiles()) {
    const parsed = parseLessonFile(filePath, course, module);
    bySlug.set(parsed.slug, parsed);
    const list = byCourse.get(course) ?? [];
    list.push(parsed);
    byCourse.set(course, list);
  }

  for (const [course, lessons] of byCourse) {
    lessons.sort(
      (a, b) => a.module.localeCompare(b.module) || a.order - b.order,
    );
    byCourse.set(course, lessons);
  }

  const courses: CourseSummary[] = Object.keys(COURSE_META).map((slug) => {
    const meta = COURSE_META[slug];
    const lessons = byCourse.get(slug) ?? [];
    const totalMinutes = lessons.reduce((sum, l) => sum + l.duration, 0);
    return {
      slug,
      title: meta.title,
      summary: meta.summary,
      category: meta.category,
      difficulty: meta.difficulty,
      duration_hours: totalMinutes
        ? Math.round((totalMinutes / 60) * 10) / 10
        : 0,
      lesson_count: lessons.length,
      tags: meta.tags,
      thumbnail: meta.thumbnail,
    };
  });

  const courseDetails = new Map<string, CourseDetail>();
  for (const summary of courses) {
    const meta = COURSE_META[summary.slug];
    const lessons = byCourse.get(summary.slug) ?? [];
    const modulesMap = new Map<string, LessonSummary[]>();
    for (const lesson of lessons) {
      const list = modulesMap.get(lesson.module) ?? [];
      list.push(toLessonSummary(lesson));
      modulesMap.set(lesson.module, list);
    }
    const modules: ModuleSummary[] = Array.from(modulesMap.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([moduleSlug, moduleLessons], idx) => ({
        slug: moduleSlug,
        title:
          MODULE_TITLES[moduleSlug] ??
          moduleSlug
            .replace(/-/g, " ")
            .replace(/\b\w/g, (ch: string) => ch.toUpperCase()),
        order: idx + 1,
        lessons: moduleLessons.sort((a, b) => a.order - b.order),
      }));

    courseDetails.set(summary.slug, {
      ...summary,
      prerequisites: meta.prerequisites,
      learning_outcomes: meta.learning_outcomes,
      modules,
      description: meta.description,
    });
  }

  const problemsDir = path.join(root, "problems");
  const problems: ProblemSummary[] = [];
  const problemsBySlug = new Map<string, ProblemDetail>();
  if (fs.existsSync(problemsDir)) {
    for (const file of fs.readdirSync(problemsDir)) {
      if (!/\.(json|ya?ml)$/.test(file)) continue;
      const data = JSON.parse(
        fs.readFileSync(path.join(problemsDir, file), "utf8"),
      ) as ProblemDetail;
      problemsBySlug.set(data.slug, data);
      problems.push({
        slug: data.slug,
        title: data.title,
        difficulty: data.difficulty,
        topics: data.topics ?? [],
        company_tags: data.company_tags ?? [],
      });
    }
  }

  return {
    root,
    builtAt: Date.now(),
    bySlug,
    byCourse,
    courses,
    courseDetails,
    problems,
    problemsBySlug,
  };
}

function getIndex(): ContentIndex {
  const root = getContentRoot();
  const now = Date.now();
  if (
    contentIndex &&
    contentIndex.root === root &&
    now - contentIndex.builtAt < CACHE_TTL_MS
  ) {
    return contentIndex;
  }
  contentIndex = buildContentIndex();
  return contentIndex;
}

export function listLessonSlugs(): string[] {
  return Array.from(getIndex().bySlug.keys());
}

export function listCourses(): CourseSummary[] {
  return getIndex().courses;
}

export function getCourse(slug: string): CourseDetail | null {
  return getIndex().courseDetails.get(slug) ?? null;
}

export function getLesson(slug: string): LessonDetail | null {
  const index = getIndex();
  const parsed = index.bySlug.get(slug);
  if (!parsed) return null;

  const ordered = index.byCourse.get(parsed.course) ?? [];
  const idx = ordered.findIndex((l) => l.slug === slug);
  return {
    ...parsed,
    previous_slug: idx > 0 ? ordered[idx - 1].slug : null,
    next_slug: idx >= 0 && idx < ordered.length - 1 ? ordered[idx + 1].slug : null,
  };
}

export function listProblems(filters?: {
  topic?: string;
  difficulty?: string;
  company?: string;
}): ProblemSummary[] {
  return getIndex().problems.filter((p) => {
    if (
      filters?.topic &&
      !p.topics.map((t) => t.toLowerCase()).includes(filters.topic.toLowerCase())
    ) {
      return false;
    }
    if (
      filters?.difficulty &&
      p.difficulty.toLowerCase() !== filters.difficulty.toLowerCase()
    ) {
      return false;
    }
    if (
      filters?.company &&
      !p.company_tags
        .map((c) => c.toLowerCase())
        .includes(filters.company.toLowerCase())
    ) {
      return false;
    }
    return true;
  });
}

export function getProblem(slug: string): ProblemDetail | null {
  return getIndex().problemsBySlug.get(slug) ?? null;
}

export function buildSearchIndex(): SearchHit[] {
  const index = getIndex();
  const hits: SearchHit[] = [];
  for (const course of index.courses) {
    hits.push({
      type: "course",
      slug: course.slug,
      title: course.title,
      summary: course.summary,
      difficulty: course.difficulty,
      score: 0,
    });
  }
  for (const lesson of index.bySlug.values()) {
    hits.push({
      type: "lesson",
      slug: lesson.slug,
      title: lesson.title,
      summary: lesson.summary,
      course: lesson.course,
      difficulty: lesson.difficulty,
      score: 0,
    });
  }
  for (const problem of index.problems) {
    hits.push({
      type: "problem",
      slug: problem.slug,
      title: problem.title,
      summary: problem.topics.join(", "),
      difficulty: problem.difficulty,
      score: 0,
    });
  }
  return hits;
}
