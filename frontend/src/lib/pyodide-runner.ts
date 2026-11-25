"use client";

export interface LocalRunResult {
  stdout: string;
  stderr: string;
  exit_code: number;
  timed_out: boolean;
  execution_time_ms: number;
  images: string[];
  truncated: boolean;
}

export interface LocalTestCase {
  name: string;
  args: Record<string, unknown>;
  expected: unknown;
  visible?: boolean;
}

export interface LocalTestResult {
  name: string;
  passed: boolean;
  visible: boolean;
  runtime_ms: number;
  expected?: string | null;
  actual?: string | null;
  error?: string | null;
}

type PyodideInterface = {
  runPythonAsync: (code: string) => Promise<unknown>;
  setStdin?: (options: { stdin: () => string | undefined }) => void;
  globals: {
    set: (key: string, value: unknown) => void;
    get: (key: string) => unknown;
  };
  loadPackage: (names: string | string[]) => Promise<void>;
};

declare global {
  interface Window {
    loadPyodide?: (opts?: { indexURL?: string }) => Promise<PyodideInterface>;
    __codecraftPyodide?: PyodideInterface;
  }
}

const PYODIDE_INDEX = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
const OUTPUT_LIMIT = 65_536;
const DEFAULT_TIMEOUT_MS = 30_000;

let loading: Promise<PyodideInterface> | null = null;

function truncate(text: string): { text: string; truncated: boolean } {
  if (text.length <= OUTPUT_LIMIT) return { text, truncated: false };
  return {
    text: `${text.slice(0, OUTPUT_LIMIT)}\n…[truncated]`,
    truncated: true,
  };
}

async function ensurePyodideScript(): Promise<void> {
  if (typeof window === "undefined") {
    throw new Error("Pyodide runs in the browser only");
  }
  if (window.loadPyodide) return;

  await new Promise<void>((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>(
      "script[data-pyodide]",
    );
    if (existing) {
      if (window.loadPyodide) {
        resolve();
        return;
      }
      existing.addEventListener("load", () => resolve());
      existing.addEventListener("error", () =>
        reject(new Error("Failed to load Pyodide")),
      );
      return;
    }
    const script = document.createElement("script");
    script.src = `${PYODIDE_INDEX}pyodide.js`;
    script.async = true;
    script.dataset.pyodide = "true";
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load Pyodide script"));
    document.head.appendChild(script);
  });
}

export async function getPyodide(): Promise<PyodideInterface> {
  if (typeof window === "undefined") {
    throw new Error("Pyodide is browser-only");
  }
  if (window.__codecraftPyodide) return window.__codecraftPyodide;
  if (!loading) {
    loading = (async () => {
      await ensurePyodideScript();
      if (!window.loadPyodide) throw new Error("loadPyodide unavailable");
      const pyodide = await window.loadPyodide({ indexURL: PYODIDE_INDEX });
      window.__codecraftPyodide = pyodide;
      return pyodide;
    })().catch((err) => {
      loading = null;
      throw err;
    });
  }
  return loading;
}

function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("TIMEOUT")), ms);
    promise
      .then((value) => {
        clearTimeout(timer);
        resolve(value);
      })
      .catch((err) => {
        clearTimeout(timer);
        reject(err);
      });
  });
}

function toJsValue(value: unknown): unknown {
  if (
    value &&
    typeof value === "object" &&
    "toJs" in value &&
    typeof (value as { toJs: (o?: object) => unknown }).toJs === "function"
  ) {
    return (value as { toJs: (o?: object) => unknown }).toJs({ depth: 5 });
  }
  return value;
}

export async function runWithPyodide(
  code: string,
  stdin = "",
  timeoutMs = DEFAULT_TIMEOUT_MS,
): Promise<LocalRunResult> {
  const start = performance.now();
  try {
    const pyodide = await getPyodide();

    // Prefer injecting stdin via StringIO — works across Pyodide versions
    const wrapper = `
import sys
from io import StringIO
_stdout = StringIO()
_stderr = StringIO()
sys.stdout = _stdout
sys.stderr = _stderr
sys.stdin = StringIO(${JSON.stringify(stdin)})
_images = []
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    def _capture_show(*args, **kwargs):
        import base64
        from io import BytesIO
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        _images.append(base64.b64encode(buf.read()).decode("ascii"))
        plt.close("all")
    plt.show = _capture_show
except Exception:
    pass
_exit = 0
try:
    exec(compile(${JSON.stringify(code)}, "<user>", "exec"), {"__name__": "__main__"})
except SystemExit as e:
    _exit = int(e.code) if isinstance(e.code, int) else 1
except Exception:
    import traceback
    traceback.print_exc()
    _exit = 1
(_stdout.getvalue(), _stderr.getvalue(), _exit, _images)
`;

    const result = await withTimeout(pyodide.runPythonAsync(wrapper), timeoutMs);
    const tuple = toJsValue(result) as [string, string, number, string[]];
    const [stdoutRaw, stderrRaw, exitCode, imagesRaw] = tuple;
    const out = truncate(String(stdoutRaw ?? ""));
    const err = truncate(String(stderrRaw ?? ""));
    return {
      stdout: out.text,
      stderr: err.text,
      exit_code: Number(exitCode) || 0,
      timed_out: false,
      execution_time_ms: performance.now() - start,
      images: Array.isArray(imagesRaw) ? imagesRaw.map(String) : [],
      truncated: out.truncated || err.truncated,
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    const timedOut = message === "TIMEOUT";
    return {
      stdout: "",
      stderr: timedOut
        ? `Execution timed out after ${timeoutMs}ms`
        : message,
      exit_code: 1,
      timed_out: timedOut,
      execution_time_ms: performance.now() - start,
      images: [],
      truncated: false,
    };
  }
}

function normalize(value: unknown): string {
  try {
    return JSON.stringify(value, (_k, v) =>
      typeof v === "bigint" ? Number(v) : v,
    );
  } catch {
    return String(value);
  }
}

export async function submitWithPyodide(
  code: string,
  functionName: string,
  tests: LocalTestCase[],
): Promise<{
  passed: boolean;
  results: LocalTestResult[];
  total: number;
  passed_count: number;
}> {
  const pyodide = await getPyodide();
  const results: LocalTestResult[] = [];

  const load = `
_user_ns = {}
exec(compile(${JSON.stringify(code)}, "<user>", "exec"), _user_ns)
_fn = _user_ns.get(${JSON.stringify(functionName)})
_fn
`;
  let fn: unknown;
  try {
    fn = await pyodide.runPythonAsync(load);
  } catch (err) {
    return {
      passed: false,
      results: [
        {
          name: "compile",
          passed: false,
          visible: true,
          runtime_ms: 0,
          error: err instanceof Error ? err.message : String(err),
        },
      ],
      total: tests.length,
      passed_count: 0,
    };
  }

  if (!fn) {
    return {
      passed: false,
      results: [
        {
          name: "compile",
          passed: false,
          visible: true,
          runtime_ms: 0,
          error: `Function ${functionName} not found`,
        },
      ],
      total: tests.length,
      passed_count: 0,
    };
  }

  for (const test of tests) {
    const started = performance.now();
    const visible = test.visible !== false;
    try {
      pyodide.globals.set("_codecraft_fn", fn);
      pyodide.globals.set("_codecraft_args", test.args);
      const actual = await withTimeout(
        pyodide.runPythonAsync(
          "args = _codecraft_args.to_py() if hasattr(_codecraft_args, 'to_py') else dict(_codecraft_args)\n_codecraft_fn(**args)",
        ),
        DEFAULT_TIMEOUT_MS,
      );
      const jsActual = toJsValue(actual);
      const ok = normalize(jsActual) === normalize(test.expected);
      results.push({
        name: test.name,
        passed: ok,
        visible,
        runtime_ms: performance.now() - started,
        expected: visible ? normalize(test.expected) : null,
        actual: visible ? normalize(jsActual) : null,
        error: ok ? null : visible ? "Output mismatch" : "Hidden test failed",
      });
    } catch (err) {
      results.push({
        name: test.name,
        passed: false,
        visible,
        runtime_ms: performance.now() - started,
        expected: visible ? normalize(test.expected) : null,
        actual: null,
        error: visible
          ? err instanceof Error
            ? err.message
            : String(err)
          : "Hidden test failed",
      });
    }
  }

  const passed_count = results.filter((r) => r.passed).length;
  return {
    passed: passed_count === results.length && results.length > 0,
    results,
    total: results.length,
    passed_count,
  };
}

/** Prefer browser Pyodide unless explicitly disabled. */
export function usePyodidePreferred(): boolean {
  return process.env.NEXT_PUBLIC_USE_PYODIDE !== "false";
}
