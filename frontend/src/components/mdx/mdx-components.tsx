import type { MDXComponents } from "mdx/types";
import {
  ComplexityTable,
  InterviewNote,
  Pitfall,
  Tip,
  Trick,
  Visualizer,
  Warning,
} from "@/components/mdx/callouts";
import { Mermaid } from "@/components/mdx/mermaid";

function Pre(props: React.HTMLAttributes<HTMLPreElement>) {
  const child = props.children as React.ReactElement | undefined;
  const className = child?.props?.className as string | undefined;
  const code = String(child?.props?.children ?? "").trim();

  if (className?.includes("language-mermaid")) {
    return <Mermaid chart={code} />;
  }

  return (
    <pre
      className="my-5 overflow-x-auto rounded-xl border border-[#333] bg-[#141414] p-4 text-[13px] leading-6 text-[#e8eaed]"
      {...props}
    />
  );
}

export const mdxComponents: MDXComponents = {
  Tip,
  Warning,
  Trick,
  InterviewNote,
  Pitfall,
  ComplexityTable,
  Visualizer,
  Mermaid,
  pre: Pre,
  h2: (props) => (
    <h2
      className="mb-3 mt-11 scroll-mt-8 border-b border-[#333] pb-2 text-[1.25rem] font-semibold tracking-tight text-white first:mt-0"
      {...props}
    />
  ),
  h3: (props) => (
    <h3
      className="mb-2 mt-8 scroll-mt-8 text-[1.05rem] font-semibold tracking-tight text-[#f5f6f8]"
      {...props}
    />
  ),
  p: (props) => (
    <p
      className="my-4 text-[16px] leading-[1.75] text-[#d7dbe3]"
      {...props}
    />
  ),
  ul: (props) => (
    <ul
      className="my-4 list-disc space-y-2 pl-6 text-[16px] leading-[1.75] text-[#d7dbe3]"
      {...props}
    />
  ),
  ol: (props) => (
    <ol
      className="my-4 list-decimal space-y-2 pl-6 text-[16px] leading-[1.75] text-[#d7dbe3]"
      {...props}
    />
  ),
  li: (props) => <li className="pl-1" {...props} />,
  a: (props) => (
    <a
      className="font-medium text-[#ffa116] underline-offset-4 hover:underline"
      target={props.href?.startsWith("http") ? "_blank" : undefined}
      rel={props.href?.startsWith("http") ? "noreferrer" : undefined}
      {...props}
    />
  ),
  table: (props) => (
    <div className="my-5 overflow-x-auto rounded-xl border border-[#333]">
      <table className="w-full border-collapse text-sm" {...props} />
    </div>
  ),
  th: (props) => (
    <th
      className="border-b border-[#333] bg-[#262626] px-3 py-2.5 text-left text-[13px] font-semibold text-white"
      {...props}
    />
  ),
  td: (props) => (
    <td
      className="border-b border-[#2a2a2a] px-3 py-2.5 align-top text-[13px] leading-6 text-[#d7dbe3]"
      {...props}
    />
  ),
  blockquote: (props) => (
    <blockquote
      className="my-5 border-l-4 border-[#ffa116]/50 bg-[#262626] px-4 py-3 text-[15px] leading-7 text-[#d7dbe3]"
      {...props}
    />
  ),
  code: (props) => {
    const isBlock = String(props.className ?? "").includes("language-");
    if (isBlock) return <code {...props} />;
    return (
      <code
        className="rounded-md bg-[#2a2a2a] px-1.5 py-0.5 font-mono text-[0.88em] text-[#ffc46b]"
        {...props}
      />
    );
  },
  hr: () => <hr className="my-10 border-[#333]" />,
};
