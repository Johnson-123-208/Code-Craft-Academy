import { notFound } from "next/navigation";
import { ProblemWorkspace } from "@/components/leetcode/problem-workspace";
import { MdxContent } from "@/components/mdx/mdx-content";
import { getProblem, listProblems } from "@/lib/content";

export function generateStaticParams() {
  return listProblems().map((p) => ({ slug: p.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }) {
  const problem = getProblem(params.slug);
  if (!problem) return { title: "Problem" };
  return { title: `${problem.title} - Practice`, description: problem.statement.slice(0, 140) };
}

export default async function ProblemPage({
  params,
}: {
  params: { slug: string };
}) {
  const problem = getProblem(params.slug);
  if (!problem) notFound();

  const all = listProblems();
  const idx = all.findIndex((p) => p.slug === problem.slug);
  const prevSlug = idx > 0 ? all[idx - 1].slug : null;
  const nextSlug = idx >= 0 && idx < all.length - 1 ? all[idx + 1].slug : null;

  return (
    <ProblemWorkspace
      problem={problem}
      problemIndex={idx >= 0 ? idx + 1 : 1}
      prevSlug={prevSlug}
      nextSlug={nextSlug}
      description={<MdxContent source={problem.statement} />}
      editorial={
        problem.editorial ? (
          <MdxContent source={problem.editorial} />
        ) : (
          <p className="text-[#eff1f699]">No editorial yet for this problem.</p>
        )
      }
    />
  );
}
