"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Loader2, Play, RotateCcw, Send } from "lucide-react";
import { CodeEditor } from "@/components/playground/code-editor";
import { runCode, submitCode } from "@/lib/api";
import {
  getPyodide,
  runWithPyodide,
  submitWithPyodide,
  usePyodidePreferred,
} from "@/lib/pyodide-runner";

const DEFAULT_CODE = `def main():
    print("Hello from CodeCraft!")


if __name__ == "__main__":
    main()
`;

interface PracticePanelProps {
  initialCode?: string;
  problemSlug?: string;
  functionName?: string;
  visibleTests?: Array<{
    name: string;
    args: Record<string, unknown>;
    expected: unknown;
  }>;
  hiddenTests?: Array<{
    name: string;
    args: Record<string, unknown>;
    expected: unknown;
  }>;
}

export function PracticePanel({
  initialCode = DEFAULT_CODE,
  problemSlug,
  functionName = "solve",
  visibleTests = [],
  hiddenTests = [],
}: PracticePanelProps) {
  const preferPyodide = usePyodidePreferred();
  const [code, setCode] = useState(initialCode || DEFAULT_CODE);
  const [stdin, setStdin] = useState("");
  const [output, setOutput] = useState(
    preferPyodide
      ? "Ctrl+Enter to run — first load warms Python in the background."
      : "Ctrl+Enter to run.",
  );
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState<"idle" | "loading" | "ok" | "err">(
    "idle",
  );
  const busyRef = useRef(false);
  const codeRef = useRef(code);
  const stdinRef = useRef(stdin);
  codeRef.current = code;
  stdinRef.current = stdin;

  useEffect(() => {
    setCode(initialCode || DEFAULT_CODE);
  }, [initialCode]);

  // Warm Pyodide as soon as the panel mounts so Run feels instant later
  useEffect(() => {
    if (!preferPyodide) return;
    let cancelled = false;
    void getPyodide()
      .then(() => {
        if (!cancelled) {
          setOutput((prev) =>
            prev.includes("warms Python") || prev.includes("Click Run")
              ? "Ready — Ctrl+Enter to run."
              : prev,
          );
        }
      })
      .catch(() => {
        /* Run will surface the error */
      });
    return () => {
      cancelled = true;
    };
  }, [preferPyodide]);

  const execute = useCallback(
    async (codeToRun: string, input: string) => {
      if (preferPyodide) {
        return runWithPyodide(codeToRun, input);
      }
      try {
        return await runCode(codeToRun, input);
      } catch {
        return runWithPyodide(codeToRun, input);
      }
    },
    [preferPyodide],
  );

  const handleRun = useCallback(async () => {
    if (busyRef.current) return;
    busyRef.current = true;
    setBusy(true);
    setStatus("loading");
    setOutput(preferPyodide ? "Running…" : "Running…");
    try {
      const result = await execute(codeRef.current, stdinRef.current);
      const failed = result.exit_code !== 0 || result.timed_out;
      setStatus(failed ? "err" : "ok");
      setOutput(
        [
          result.stdout || "",
          result.stderr || "",
          result.timed_out ? "Timed out." : "",
          `exit=${result.exit_code} · ${Number(result.execution_time_ms).toFixed(0)} ms`,
        ]
          .filter(Boolean)
          .join("\n"),
      );
    } catch (err) {
      setStatus("err");
      setOutput(err instanceof Error ? err.message : "Execution failed");
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
  }, [execute, preferPyodide]);

  const handleSubmit = useCallback(async () => {
    if (!problemSlug || busyRef.current) {
      if (!problemSlug) {
        setOutput("Open a practice problem to use Submit.");
        setStatus("err");
      }
      return;
    }
    busyRef.current = true;
    setBusy(true);
    setStatus("loading");
    setOutput("Submitting…");
    try {
      if (preferPyodide && (visibleTests.length > 0 || hiddenTests.length > 0)) {
        const tests = [
          ...visibleTests.map((t) => ({ ...t, visible: true })),
          ...hiddenTests.map((t) => ({ ...t, visible: false })),
        ];
        const result = await submitWithPyodide(
          codeRef.current,
          functionName,
          tests,
        );
        setStatus(result.passed ? "ok" : "err");
        setOutput(
          [
            result.passed ? "Accepted" : "Wrong Answer",
            `passed ${result.passed_count}/${result.total}`,
            ...result.results.map((r) =>
              r.passed
                ? `✓ ${r.name}`
                : `✗ ${r.name}${r.visible ? ` — ${r.error ?? "mismatch"}` : " — Hidden test failed"}`,
            ),
          ].join("\n"),
        );
      } else {
        const result = await submitCode(problemSlug, codeRef.current);
        setStatus(result.passed ? "ok" : "err");
        setOutput(
          [
            result.passed ? "Accepted" : "Wrong Answer",
            ...(result.results?.map(
              (r: { name: string; passed: boolean; error?: string }) =>
                `${r.passed ? "✓" : "✗"} ${r.name}${r.error ? ` — ${r.error}` : ""}`,
            ) ?? []),
          ].join("\n"),
        );
      }
    } catch (err) {
      setStatus("err");
      setOutput(err instanceof Error ? err.message : "Submit failed");
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
  }, [
    functionName,
    hiddenTests,
    preferPyodide,
    problemSlug,
    visibleTests,
  ]);

  // Panel-level shortcut (editor + stdin focus)
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (!(e.ctrlKey || e.metaKey) || e.key !== "Enter") return;
      e.preventDefault();
      if (e.shiftKey) void handleSubmit();
      else void handleRun();
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [handleRun, handleSubmit]);

  return (
    <div className="flex h-full min-h-0 flex-col overflow-hidden bg-[#1a1a1a] text-[#eff1f6]">
      <div className="flex shrink-0 flex-wrap items-center gap-2 border-b border-[#333] bg-[#262626] px-3 py-2">
        <span className="mr-auto rounded bg-[#333] px-2 py-0.5 text-[11px] font-medium">
          Python3 {preferPyodide ? "· Browser" : "· API"}
        </span>
        <kbd className="hidden rounded border border-[#444] bg-[#1a1a1a] px-1.5 py-0.5 font-mono text-[10px] text-[#eff1f666] sm:inline">
          Ctrl+Enter
        </kbd>
        <button
          type="button"
          onClick={() => setCode(initialCode || DEFAULT_CODE)}
          disabled={busy}
          className="inline-flex h-8 items-center gap-1 rounded-lg px-2.5 text-xs hover:bg-[#333] disabled:opacity-50"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          Reset
        </button>
        <button
          type="button"
          onClick={() => void handleRun()}
          disabled={busy}
          title="Ctrl+Enter"
          className="inline-flex h-8 items-center gap-1 rounded-lg bg-[#2cbb5d] px-3 text-xs font-semibold text-white hover:bg-[#25a352] disabled:opacity-60"
        >
          {busy ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
          ) : (
            <Play className="h-3.5 w-3.5 fill-current" />
          )}
          Run
        </button>
        <button
          type="button"
          onClick={() => void handleSubmit()}
          disabled={busy || !problemSlug}
          title="Ctrl+Shift+Enter"
          className="inline-flex h-8 items-center gap-1 rounded-lg bg-[#ffa116] px-3 text-xs font-semibold text-[#1a1a1a] hover:bg-[#ffb84d] disabled:opacity-40"
        >
          <Send className="h-3.5 w-3.5" />
          Submit
        </button>
      </div>

      <div className="min-h-0 flex-[1.4]">
        <CodeEditor
          value={code}
          onChange={setCode}
          onRun={handleRun}
          onSubmit={problemSlug ? handleSubmit : undefined}
        />
      </div>

      <div className="grid shrink-0 grid-rows-2 border-t border-[#333] sm:grid-rows-1 sm:grid-cols-2">
        <label className="block border-b border-[#333] p-2 text-[11px] text-[#eff1f666] sm:border-b-0 sm:border-r">
          stdin
          <textarea
            value={stdin}
            onChange={(e) => setStdin(e.target.value)}
            className="mt-1 h-20 w-full resize-none rounded-md border border-[#333] bg-[#111] p-2 font-mono text-xs text-[#eff1f6] outline-none"
            spellCheck={false}
          />
        </label>
        <label className="block p-2 text-[11px] text-[#eff1f666]">
          Result
          <pre
            className={
              "mt-1 h-20 overflow-auto rounded-md border border-[#333] bg-[#111] p-2 font-mono text-xs " +
              (status === "ok"
                ? "text-[#2cbb5d]"
                : status === "err"
                  ? "text-[#ff375f]"
                  : "text-[#eff1f6]")
            }
          >
            {output}
          </pre>
        </label>
      </div>
    </div>
  );
}
