"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Code2,
  FileText,
  Lightbulb,
  Loader2,
  Play,
  RotateCcw,
  BookOpen,
  XCircle,
} from "lucide-react";
import { CodeEditor } from "@/components/playground/code-editor";
import { DifficultyText } from "@/components/leetcode/difficulty";
import { Button } from "@/components/ui/button";
import { runCode, submitCode } from "@/lib/api";
import {
  getPyodide,
  runWithPyodide,
  submitWithPyodide,
  usePyodidePreferred,
} from "@/lib/pyodide-runner";
import type { ProblemDetail } from "@/types/content";
import { cn } from "@/lib/utils";

type LeftTab = "description" | "editorial" | "hints";
type BottomTab = "testcase" | "result";

interface ProblemWorkspaceProps {
  problem: ProblemDetail;
  problemIndex: number;
  prevSlug?: string | null;
  nextSlug?: string | null;
  description: React.ReactNode;
  editorial: React.ReactNode;
}

export function ProblemWorkspace({
  problem,
  problemIndex,
  prevSlug,
  nextSlug,
  description,
  editorial,
}: ProblemWorkspaceProps) {
  const preferPyodide = usePyodidePreferred();
  const [leftTab, setLeftTab] = useState<LeftTab>("description");
  const [bottomTab, setBottomTab] = useState<BottomTab>("testcase");
  const [code, setCode] = useState(problem.starter_code);
  const [busy, setBusy] = useState(false);
  const [activeCase, setActiveCase] = useState(0);
  const [split, setSplit] = useState(46);
  const dragging = useRef(false);
  const busyRef = useRef(false);
  const codeRef = useRef(code);
  codeRef.current = code;
  const [resultStatus, setResultStatus] = useState<
    "idle" | "accepted" | "wrong" | "error" | "running"
  >("idle");
  const [resultLines, setResultLines] = useState<string[]>([]);
  const [runtimeMs, setRuntimeMs] = useState<number | null>(null);
  const [hintOpen, setHintOpen] = useState<number[]>([]);

  const cases = problem.visible_tests ?? [];

  useEffect(() => {
    setCode(problem.starter_code);
    setResultStatus("idle");
    setResultLines([]);
    setActiveCase(0);
    setLeftTab("description");
    setHintOpen([]);
  }, [problem.slug, problem.starter_code]);

  const caseArgsText = useMemo(() => {
    const c = cases[activeCase];
    if (!c) return "";
    return Object.entries(c.args)
      .map(([k, v]) => `${k} = ${JSON.stringify(v)}`)
      .join("\n");
  }, [cases, activeCase]);

  const onMouseMove = useCallback((e: MouseEvent) => {
    if (!dragging.current) return;
    const pct = (e.clientX / window.innerWidth) * 100;
    setSplit(Math.min(70, Math.max(28, pct)));
  }, []);

  const onMouseUp = useCallback(() => {
    dragging.current = false;
    document.body.style.cursor = "";
    document.body.style.userSelect = "";
  }, []);

  useEffect(() => {
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };
  }, [onMouseMove, onMouseUp]);

  useEffect(() => {
    if (!preferPyodide) return;
    void getPyodide().catch(() => undefined);
  }, [preferPyodide]);

  const handleRun = useCallback(async () => {
    if (busyRef.current) return;
    busyRef.current = true;
    setBusy(true);
    setResultStatus("running");
    setBottomTab("result");
    const started = performance.now();
    const currentCode = codeRef.current;
    try {
      const c = cases[activeCase];
      if (preferPyodide && c && problem.function_name) {
        const result = await submitWithPyodide(
          currentCode,
          problem.function_name,
          [{ ...c, visible: true }],
        );
        const r = result.results[0];
        setRuntimeMs(performance.now() - started);
        if (r?.passed) {
          setResultStatus("accepted");
          setResultLines([
            "Accepted",
            `Runtime: ${(performance.now() - started).toFixed(0)} ms`,
            `Case: ${c.name}`,
            `Input:\n${caseArgsText}`,
            `Output: ${r.actual ?? ""}`,
            `Expected: ${r.expected ?? ""}`,
          ]);
        } else {
          setResultStatus("wrong");
          setResultLines(
            [
              "Wrong Answer",
              `Case: ${c.name}`,
              `Input:\n${caseArgsText}`,
              `Output: ${r?.actual ?? "n/a"}`,
              `Expected: ${r?.expected ?? "n/a"}`,
              r?.error ? `Error: ${r.error}` : "",
            ].filter(Boolean),
          );
        }
      } else {
        const result = preferPyodide
          ? await runWithPyodide(currentCode, "")
          : await runCode(currentCode, "");
        setRuntimeMs(Number(result.execution_time_ms));
        setResultStatus(result.exit_code === 0 ? "accepted" : "error");
        setResultLines(
          [
            result.exit_code === 0 ? "Finished" : "Runtime Error",
            result.stdout,
            result.stderr,
            `Runtime: ${Number(result.execution_time_ms).toFixed(0)} ms`,
          ].filter(Boolean),
        );
      }
    } catch (err) {
      setResultStatus("error");
      setResultLines([err instanceof Error ? err.message : "Run failed"]);
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
  }, [
    activeCase,
    caseArgsText,
    cases,
    preferPyodide,
    problem.function_name,
  ]);

  const handleSubmit = useCallback(async () => {
    if (busyRef.current) return;
    busyRef.current = true;
    setBusy(true);
    setResultStatus("running");
    setBottomTab("result");
    const started = performance.now();
    const currentCode = codeRef.current;
    try {
      if (preferPyodide && cases.length > 0) {
        const result = await submitWithPyodide(
          currentCode,
          problem.function_name ?? "solve",
          cases.map((t) => ({ ...t, visible: true })),
        );
        setRuntimeMs(performance.now() - started);
        if (result.passed) {
          setResultStatus("accepted");
          setResultLines([
            "Accepted",
            `Runtime: ${(performance.now() - started).toFixed(0)} ms`,
            `Tests passed: ${result.passed_count}/${result.total}`,
            ...result.results.map((r) => `✓ ${r.name}`),
          ]);
        } else {
          setResultStatus("wrong");
          setResultLines([
            "Wrong Answer",
            `Passed ${result.passed_count}/${result.total} visible tests`,
            ...result.results.map((r) =>
              r.passed
                ? `✓ ${r.name}`
                : `✗ ${r.name}${r.expected != null ? ` — expected ${r.expected}, got ${r.actual}` : ""}`,
            ),
          ]);
        }
      } else {
        const result = await submitCode(problem.slug, currentCode);
        setRuntimeMs(performance.now() - started);
        setResultStatus(result.passed ? "accepted" : "wrong");
        setResultLines([
          result.passed ? "Accepted" : "Wrong Answer",
          `Passed ${result.passed_count}/${result.total}`,
          ...(result.results?.map(
            (r: { name: string; passed: boolean; error?: string }) =>
              `${r.passed ? "✓" : "✗"} ${r.name}${r.error ? ` — ${r.error}` : ""}`,
          ) ?? []),
        ]);
      }
    } catch (err) {
      setResultStatus("error");
      setResultLines([err instanceof Error ? err.message : "Submit failed"]);
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
  }, [cases, preferPyodide, problem.function_name, problem.slug]);

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
    <div className="lc-workspace flex h-screen flex-col bg-[#1a1a1a] text-[#eff1f6]">
      <div className="flex h-12 shrink-0 items-center gap-2 border-b border-[#333] bg-[#262626] px-3">
        <Link
          href="/practice"
          className="inline-flex items-center gap-1 rounded px-2 py-1 text-sm text-[#eff1f6bb] hover:bg-[#333] hover:text-white"
        >
          <Code2 className="h-4 w-4 text-[#ffa116]" />
          Problem List
        </Link>
        <div className="mx-1 h-4 w-px bg-[#444]" />
        {prevSlug ? (
          <Link
            href={`/practice/${prevSlug}`}
            className="rounded p-1 hover:bg-[#333]"
            aria-label="Previous"
          >
            <ChevronLeft className="h-4 w-4" />
          </Link>
        ) : (
          <span className="p-1 opacity-30">
            <ChevronLeft className="h-4 w-4" />
          </span>
        )}
        {nextSlug ? (
          <Link
            href={`/practice/${nextSlug}`}
            className="rounded p-1 hover:bg-[#333]"
            aria-label="Next"
          >
            <ChevronRight className="h-4 w-4" />
          </Link>
        ) : (
          <span className="p-1 opacity-30">
            <ChevronRight className="h-4 w-4" />
          </span>
        )}
        <div className="ml-auto flex items-center gap-2">
          <Button
            size="sm"
            variant="ghost"
            className="h-8 text-[#eff1f6] hover:bg-[#333]"
            onClick={() => setCode(problem.starter_code)}
            disabled={busy}
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Reset
          </Button>
          <kbd className="hidden rounded border border-[#444] bg-[#1a1a1a] px-1.5 py-0.5 font-mono text-[10px] text-[#eff1f666] md:inline">
            Ctrl+Enter
          </kbd>
          <Button
            size="sm"
            className="h-8 bg-[#2cbb5d] text-white hover:bg-[#25a352]"
            onClick={() => void handleRun()}
            disabled={busy}
            title="Ctrl+Enter"
          >
            {busy && resultStatus === "running" ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
            ) : (
              <Play className="h-3.5 w-3.5 fill-current" />
            )}
            Run
          </Button>
          <Button
            size="sm"
            className="h-8 bg-[#ffa116] font-semibold text-[#1a1a1a] hover:bg-[#ffb84d]"
            onClick={() => void handleSubmit()}
            disabled={busy}
            title="Ctrl+Shift+Enter"
          >
            Submit
          </Button>
        </div>
      </div>

      <div className="flex min-h-0 flex-1">
        <aside
          className="flex min-w-0 flex-col border-r border-[#333] bg-[#262626]"
          style={{ width: `${split}%` }}
        >
          <div className="flex shrink-0 gap-1 border-b border-[#333] px-2 pt-2">
            {(
              [
                ["description", FileText, "Description"],
                ["editorial", BookOpen, "Editorial"],
                ["hints", Lightbulb, "Hints"],
              ] as const
            ).map(([id, Icon, label]) => (
              <button
                key={id}
                type="button"
                onClick={() => setLeftTab(id)}
                className={cn(
                  "inline-flex items-center gap-1.5 rounded-t-md px-3 py-2 text-sm",
                  leftTab === id
                    ? "bg-[#1a1a1a] text-white"
                    : "text-[#eff1f6aa] hover:text-white",
                )}
              >
                <Icon className="h-3.5 w-3.5" />
                {label}
              </button>
            ))}
          </div>

          <div className="lc-scroll min-h-0 flex-1 overflow-y-auto px-5 py-4">
            {leftTab === "description" && (
              <div>
                <h1 className="text-xl font-semibold text-white">
                  {problemIndex}. {problem.title}
                </h1>
                <div className="mt-3 flex flex-wrap items-center gap-3">
                  <DifficultyText difficulty={problem.difficulty} />
                  <span className="text-xs text-[#eff1f666]">Python3</span>
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {problem.topics.map((t) => (
                    <span
                      key={t}
                      className="rounded-full bg-[#333] px-2.5 py-0.5 text-xs text-[#eff1f6cc]"
                    >
                      {t}
                    </span>
                  ))}
                  {problem.company_tags.map((c) => (
                    <span
                      key={c}
                      className="rounded-full border border-[#444] px-2.5 py-0.5 text-xs text-[#eff1f699]"
                    >
                      {c}
                    </span>
                  ))}
                </div>

                <div className="lc-prose mt-6">{description}</div>

                <div className="mt-8 space-y-4">
                  {problem.examples.map((ex, i) => (
                    <div key={i}>
                      <p className="mb-2 text-sm font-semibold text-white">
                        Example {i + 1}:
                      </p>
                      <div className="rounded-lg bg-[#1a1a1a] p-3 font-mono text-[13px] leading-6">
                        <p>
                          <span className="text-[#eff1f699]">Input: </span>
                          <span>{ex.input}</span>
                        </p>
                        <p>
                          <span className="text-[#eff1f699]">Output: </span>
                          <span>{ex.output}</span>
                        </p>
                        {ex.explanation && (
                          <p className="mt-1 font-sans text-[13px]">
                            <span className="font-mono text-[#eff1f699]">
                              Explanation:{" "}
                            </span>
                            <span className="text-[#eff1f6bb]">{ex.explanation}</span>
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {problem.constraints.length > 0 && (
                  <div className="mt-8">
                    <p className="mb-2 text-sm font-semibold text-white">
                      Constraints:
                    </p>
                    <ul className="list-disc space-y-1.5 pl-5 text-sm">
                      {problem.constraints.map((c) => (
                        <li key={c}>
                          <code className="rounded bg-[#333] px-1.5 py-0.5 font-mono text-[12px] text-[#ffa116]">
                            {c}
                          </code>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {leftTab === "editorial" && (
              <div>
                <h2 className="mb-4 text-lg font-semibold text-white">Solution</h2>
                <div className="lc-prose">{editorial}</div>
                {problem.approaches?.length > 0 && (
                  <div className="mt-6 space-y-3">
                    <h3 className="font-semibold text-white">Approaches</h3>
                    {problem.approaches.map((a, i) => (
                      <div key={i} className="rounded-lg border border-[#333] p-3">
                        <p className="font-medium text-[#ffa116]">
                          {String(a.name ?? `Approach ${i + 1}`)}
                        </p>
                        <p className="mt-1 text-sm text-[#eff1f6bb]">
                          {String(a.explanation ?? "")}
                        </p>
                        {a.complexity != null && (
                          <p className="mt-2 font-mono text-xs text-[#00b8a3]">
                            {JSON.stringify(a.complexity)}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {leftTab === "hints" && (
              <div className="space-y-3">
                <h2 className="text-lg font-semibold text-white">Hints</h2>
                {problem.hints.length === 0 && (
                  <p className="text-sm text-[#eff1f699]">No hints for this problem.</p>
                )}
                {problem.hints.map((h, i) => {
                  const open = hintOpen.includes(i);
                  return (
                    <div key={i} className="rounded-lg border border-[#333]">
                      <button
                        type="button"
                        className="flex w-full items-center justify-between px-3 py-2 text-left text-sm font-medium hover:bg-[#333]/60"
                        onClick={() =>
                          setHintOpen((prev) =>
                            open ? prev.filter((x) => x !== i) : [...prev, i],
                          )
                        }
                      >
                        Hint {i + 1}
                        <span className="text-[#eff1f666]">
                          {open ? "Hide" : "Show"}
                        </span>
                      </button>
                      {open && (
                        <p className="border-t border-[#333] px-3 py-3 text-sm leading-6 text-[#eff1f6bb]">
                          {h}
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </aside>

        <div
          role="separator"
          aria-orientation="vertical"
          className="w-1.5 shrink-0 cursor-col-resize bg-[#1a1a1a] hover:bg-[#ffa116]/80"
          onMouseDown={() => {
            dragging.current = true;
            document.body.style.cursor = "col-resize";
            document.body.style.userSelect = "none";
          }}
        />

        <section className="flex min-w-0 flex-1 flex-col bg-[#1a1a1a]">
          <div className="flex h-10 shrink-0 items-center gap-2 border-b border-[#333] bg-[#262626] px-3">
            <span className="rounded bg-[#333] px-2 py-0.5 text-xs font-medium">
              Python3
            </span>
            <span className="text-xs text-[#eff1f666]">
              {preferPyodide ? "Pyodide runtime" : "API sandbox"}
            </span>
          </div>

          <div className="min-h-0 flex-[1.2]">
            <CodeEditor
              value={code}
              onChange={setCode}
              onRun={handleRun}
              onSubmit={handleSubmit}
            />
          </div>

          <div className="flex min-h-[190px] max-h-[40%] flex-col border-t border-[#333] bg-[#262626]">
            <div className="flex items-center gap-1 border-b border-[#333] px-2">
              {(
                [
                  ["testcase", "Testcase"],
                  ["result", "Test Result"],
                ] as const
              ).map(([id, label]) => (
                <button
                  key={id}
                  type="button"
                  onClick={() => setBottomTab(id)}
                  className={cn(
                    "px-3 py-2 text-sm",
                    bottomTab === id
                      ? "border-b-2 border-[#ffa116] text-white"
                      : "text-[#eff1f6aa]",
                  )}
                >
                  {label}
                </button>
              ))}
              {resultStatus === "accepted" && (
                <span className="ml-auto inline-flex items-center gap-1 px-2 text-sm font-medium text-[#2cbb5d]">
                  <CheckCircle2 className="h-4 w-4" /> Accepted
                  {runtimeMs != null && (
                    <span className="text-[#eff1f666]">
                      {" "}
                      · {runtimeMs.toFixed(0)} ms
                    </span>
                  )}
                </span>
              )}
              {resultStatus === "wrong" && (
                <span className="ml-auto inline-flex items-center gap-1 px-2 text-sm font-medium text-[#ff375f]">
                  <XCircle className="h-4 w-4" /> Wrong Answer
                </span>
              )}
            </div>

            <div className="min-h-0 flex-1 overflow-auto p-3">
              {bottomTab === "testcase" && (
                <div>
                  <div className="mb-3 flex flex-wrap gap-2">
                    {cases.length === 0 && (
                      <p className="text-sm text-[#eff1f699]">No visible testcases.</p>
                    )}
                    {cases.map((c, i) => (
                      <button
                        key={c.name}
                        type="button"
                        onClick={() => setActiveCase(i)}
                        className={cn(
                          "rounded-lg px-3 py-1.5 text-xs font-medium",
                          activeCase === i
                            ? "bg-[#333] text-white"
                            : "text-[#eff1f6aa] hover:bg-[#333]/70",
                        )}
                      >
                        Case {i + 1}
                      </button>
                    ))}
                  </div>
                  {cases[activeCase] && (
                    <pre className="whitespace-pre-wrap rounded-lg bg-[#1a1a1a] p-3 font-mono text-[13px] leading-6">
                      {caseArgsText}
                      {"\n"}
                      <span className="text-[#eff1f666]">
                        expected = {JSON.stringify(cases[activeCase].expected)}
                      </span>
                    </pre>
                  )}
                </div>
              )}
              {bottomTab === "result" && (
                <pre
                  className={cn(
                    "whitespace-pre-wrap font-mono text-[13px] leading-6",
                    resultStatus === "accepted" && "text-[#2cbb5d]",
                    resultStatus === "wrong" && "text-[#ff375f]",
                    resultStatus === "error" && "text-[#ffa116]",
                    resultStatus === "idle" && "text-[#eff1f699]",
                    resultStatus === "running" && "text-[#eff1f6]",
                  )}
                >
                  {resultStatus === "idle"
                    ? "Run or Submit to see results."
                    : resultStatus === "running"
                      ? "Running..."
                      : resultLines.join("\n")}
                </pre>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
