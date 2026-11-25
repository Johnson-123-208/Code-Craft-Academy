import { CourseCard } from "@/components/course/course-card";
import { listCourses } from "@/lib/content";

export const metadata = {
  title: "Explore",
  description: "Browse CodeCraft courses — LeetCode-style learning paths.",
};

export default function CatalogPage({
  searchParams,
}: {
  searchParams?: { category?: string; difficulty?: string; topic?: string };
}) {
  let courses = listCourses();
  const category = searchParams?.category?.toLowerCase();
  const difficulty = searchParams?.difficulty?.toLowerCase();
  const topic = searchParams?.topic?.toLowerCase();

  if (category) {
    courses = courses.filter((c) => c.category.toLowerCase().includes(category));
  }
  if (difficulty) {
    courses = courses.filter((c) => c.difficulty.toLowerCase() === difficulty);
  }
  if (topic) {
    courses = courses.filter((c) =>
      c.tags.some((t) => t.toLowerCase().includes(topic)),
    );
  }

  const categories = Array.from(new Set(listCourses().map((c) => c.category)));

  return (
    <div className="min-h-[calc(100vh-3rem)] bg-[#1a1a1a] text-[#eff1f6]">
      <div className="mx-auto max-w-[1400px] px-4 py-10 sm:px-6">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#ffa116]">
          Explore
        </p>
        <h1 className="mt-1 text-3xl font-semibold text-white">Courses</h1>
        <p className="mt-2 text-sm text-[#eff1f699]">
          Study plans that pair with the problemset workspace.
        </p>

        <form
          className="mt-6 flex flex-wrap gap-2 rounded-xl border border-[#333] bg-[#262626] p-3"
          method="get"
        >
          <select
            name="category"
            defaultValue={searchParams?.category ?? ""}
            className="h-9 rounded-lg border border-[#333] bg-[#1a1a1a] px-3 text-sm text-white"
          >
            <option value="">Category</option>
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          <select
            name="difficulty"
            defaultValue={searchParams?.difficulty ?? ""}
            className="h-9 rounded-lg border border-[#333] bg-[#1a1a1a] px-3 text-sm text-white"
          >
            <option value="">Difficulty</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <input
            name="topic"
            defaultValue={searchParams?.topic ?? ""}
            placeholder="Topic tag"
            className="h-9 rounded-lg border border-[#333] bg-[#1a1a1a] px-3 text-sm text-white placeholder:text-[#eff1f644]"
          />
          <button
            type="submit"
            className="h-9 rounded-lg bg-[#ffa116] px-4 text-sm font-semibold text-[#1a1a1a]"
          >
            Apply
          </button>
        </form>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {courses.map((course) => (
            <CourseCard key={course.slug} course={course} />
          ))}
        </div>
        {courses.length === 0 && (
          <p className="mt-10 text-[#eff1f666]">No courses match those filters.</p>
        )}
      </div>
    </div>
  );
}
