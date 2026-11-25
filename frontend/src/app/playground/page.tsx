"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Loader2, Play, RotateCcw } from "lucide-react";
import { CodeEditor } from "@/components/playground/code-editor";
import { runCode } from "@/lib/api";
import {
  getPyodide,
  runWithPyodide,
  usePyodidePreferred,
} from "@/lib/pyodide-runner";

const DEFAULT = `# CodeCraft Playground
from math import sqrt

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

print([n for n in range(30) if is_prime(n)])
`;

export default function PlaygroundPage() {
  const preferPyodide = usePyodidePreferred();
  const [code, setCode] = useState(DEFAULT);
  const [stdin, setStdin] = useState("");
  const [output, setOutput] = useState(
    preferPyodide
      ? "Ctrl+Enter to run — warming Python…"
      : "Ctrl+Enter to run.",
  );
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);
  const codeRef = useRef(code);
  const stdinRef = useRef(stdin);
  codeRef.current = code;
  stdinRef.current = stdin;

  useEffect(() => {
    if (!preferPyodide) return;
    void getPyodide()
      .then(() => setOutput("Ready — Ctrl+Enter to run."))
      .catch(() => undefined);
  }, [preferPyodide]);

  const handleRun = useCallback(async () => {
    if (busyRef.current) return;
    busyRef.current = true;
    setBusy(true);
    setOutput("Running…");
    try {
      const result = preferPyodide
        ? await runWithPyodide(codeRef.current, stdinRef.current)
        : await runCode(codeRef.current, stdinRef.current);
      setOutput(
        [
          result.stdout,
          result.stderr,
          `exit=${result.exit_code} · ${Number(result.execution_time_ms).toFixed(0)} ms`,
        ]
          .filter(Boolean)
          .join("\n"),
      );
    } catch (err) {
      setOutput(err instanceof Error ? err.message : "Run failed");
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
  }, [preferPyodide]);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        void handleRun();
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [handleRun]);

  return (
    <div className="flex h-[calc(100vh-3rem)] flex-col bg-[#1a1a1a] text-[#eff1f6]">
      <div className="flex h-12 shrink-0 items-center gap-3 border-b border-[#333] bg-[#262626] px-4">
        <h1 className="text-sm font-semibold text-white">Playground</h1>
        <span className="rounded bg-[#333] px-2 py-0.5 text-[11px]">Python3</span>
        <kbd className="hidden rounded border border-[#444] bg-[#1a1a1a] px-1.5 py-0.5 font-mono text-[10px] text-[#eff1f666] sm:inline">
          Ctrl+Enter
        </kbd>
        <div className="ml-auto flex gap-2">
          <button
            type="button"
            onClick={() => setCode(DEFAULT)}
            className="inline-flex h-8 items-center gap-1.5 rounded-lg px-3 text-xs text-[#eff1f6] hover:bg-[#333]"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Reset
          </button>
          <button
            type="button"
            onClick={() => void handleRun()}
            disabled={busy}
            title="Ctrl+Enter"
            className="inline-flex h-8 items-center gap-1.5 rounded-lg bg-[#2cbb5d] px-3 text-xs font-semibold text-white hover:bg-[#25a352] disabled:opacity-60"
          >
            {busy ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
            ) : (
              <Play className="h-3.5 w-3.5 fill-current" />
            )}
            Run
          </button>
        </div>
      </div>

      <div className="grid min-h-0 flex-1 lg:grid-cols-[1fr_340px]">
        <div className="min-h-[320px] border-r border-[#333]">
          <CodeEditor value={code} onChange={setCode} onRun={handleRun} />
        </div>
        <div className="flex min-h-[220px] flex-col bg-[#262626]">
          <div className="border-b border-[#333] px-3 py-2 text-xs font-medium text-[#eff1f6aa]">
            stdin
          </div>
          <textarea
            value={stdin}
            onChange={(e) => setStdin(e.target.value)}
            className="h-28 resize-none border-b border-[#333] bg-[#1a1a1a] p-3 font-mono text-xs text-[#eff1f6] outline-none"
          />
          <div className="border-b border-[#333] px-3 py-2 text-xs font-medium text-[#eff1f6aa]">
            Console
          </div>
          <pre className="min-h-0 flex-1 overflow-auto p-3 font-mono text-xs leading-5 text-[#eff1f6]">
            {output}
          </pre>
        </div>
      </div>
    </div>
  );
}
