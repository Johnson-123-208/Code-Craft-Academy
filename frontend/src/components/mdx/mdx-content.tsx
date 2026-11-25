import { MDXRemote } from "next-mdx-remote/rsc";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypeKatex from "rehype-katex";
import { mdxComponents } from "@/components/mdx/mdx-components";

export async function MdxContent({ source }: { source: string }) {
  return (
    <article className="mdx-content max-w-none">
      <MDXRemote
        source={source}
        components={mdxComponents}
        options={{
          mdxOptions: {
            remarkPlugins: [remarkGfm, remarkMath],
            rehypePlugins: [
              rehypeSlug,
              [rehypeAutolinkHeadings, { behavior: "wrap" }],
              rehypeKatex,
            ],
          },
        }}
      />
    </article>
  );
}
