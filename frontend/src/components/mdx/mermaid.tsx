"use client";

import { useEffect, useId, useState } from "react";
import { useTheme } from "next-themes";

interface MermaidProps {
  chart: string;
}

export function Mermaid({ chart }: MermaidProps) {
  const id = useId().replace(/:/g, "");
  const { resolvedTheme } = useTheme();
  const [svg, setSvg] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function render() {
      try {
        const mermaid = (await import("mermaid")).default;
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: "strict",
          theme: resolvedTheme === "dark" ? "dark" : "default",
          fontFamily: "var(--font-sans)",
        });
        const { svg: rendered } = await mermaid.render(
          `mermaid-${id}`,
          chart.trim(),
        );
        if (!cancelled) {
          setSvg(rendered);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to render diagram");
        }
      }
    }

    void render();
    return () => {
      cancelled = true;
    };
  }, [chart, id, resolvedTheme]);

  if (error) {
    return (
      <pre className="my-6 overflow-x-auto rounded-lg border border-rose-500/40 bg-rose-500/10 p-4 text-xs text-rose-700 dark:text-rose-300">
        Mermaid error: {error}
      </pre>
    );
  }

  return (
    <div
      className="my-6 overflow-x-auto rounded-lg border border-border bg-muted/30 p-4 [&_svg]:mx-auto"
      dangerouslySetInnerHTML={svg ? { __html: svg } : undefined}
      aria-label="Diagram"
    />
  );
}
