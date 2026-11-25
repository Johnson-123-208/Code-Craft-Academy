"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import {
  Code2,
  List,
  PanelLeftClose,
  PanelRightClose,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

export function LessonWorkspace({
  breadcrumb,
  outline,
  content,
  practice,
}: {
  breadcrumb: React.ReactNode;
  outline: React.ReactNode;
  content: React.ReactNode;
  practice: React.ReactNode;
}) {
  const [showOutline, setShowOutline] = useState(true);
  const [showCode, setShowCode] = useState(false);
  const [mobileOutline, setMobileOutline] = useState(false);
  const [codePct, setCodePct] = useState(40);
  const splitRef = useRef<HTMLDivElement>(null);
  const dragging = useRef(false);

  const openCode = useCallback(() => setShowCode(true), []);
  const closeCode = useCallback(() => setShowCode(false), []);
  const toggleCode = useCallback(() => setShowCode((v) => !v), []);

  const onMouseMove = useCallback((e: MouseEvent) => {
    if (!dragging.current || !splitRef.current) return;
    const rect = splitRef.current.getBoundingClientRect();
    if (rect.width <= 0) return;
    const fromRight = rect.right - e.clientX;
    const pct = (fromRight / rect.width) * 100;
    setCodePct(Math.min(62, Math.max(28, pct)));
  }, []);

  const onMouseUp = useCallback(() => {
    if (!dragging.current) return;
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

  function startResize() {
    dragging.current = true;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
  }

  const interpreterButton = (
    <button
      type="button"
      onClick={toggleCode}
      className={cn(
        "flex w-full items-center justify-center gap-2 rounded-md px-3 py-2 text-xs font-semibold transition",
        showCode
          ? "border border-[#444] bg-[#2a2a2a] text-white hover:bg-[#333]"
          : "bg-[#2cbb5d] text-white hover:bg-[#25a352]",
      )}
      aria-pressed={showCode}
    >
      {showCode ? (
        <>
          <PanelRightClose className="h-3.5 w-3.5" />
          Close interpreter
        </>
      ) : (
        <>
          <Code2 className="h-3.5 w-3.5" />
          Open interpreter
        </>
      )}
    </button>
  );

  return (
    <div className="flex h-full min-h-0 flex-col overflow-hidden bg-[#1a1a1a]">
      {/* Single compact top bar */}
      <div className="flex h-9 shrink-0 items-center gap-2 border-b border-[#333] bg-[#262626] px-2">
        <Link
          href="/"
          className="flex h-6 w-6 shrink-0 items-center justify-center rounded bg-[#ffa116] text-[11px] font-black text-[#1a1a1a]"
          aria-label="CodeCraft home"
        >
          C
        </Link>

        <button
          type="button"
          onClick={() => setShowOutline((v) => !v)}
          className="hidden h-7 items-center gap-1 rounded px-1.5 text-[11px] text-[#eff1f6aa] hover:bg-[#333] hover:text-white lg:inline-flex"
          aria-pressed={showOutline}
          title="Toggle lessons"
        >
          {showOutline ? (
            <PanelLeftClose className="h-3.5 w-3.5" />
          ) : (
            <List className="h-3.5 w-3.5" />
          )}
          <span className="sr-only sm:not-sr-only">Lessons</span>
        </button>

        <button
          type="button"
          onClick={() => setMobileOutline(true)}
          className="inline-flex h-7 items-center gap-1 rounded px-1.5 text-[11px] text-[#eff1f6aa] hover:bg-[#333] hover:text-white lg:hidden"
        >
          <List className="h-3.5 w-3.5" />
          Lessons
        </button>

        <div className="min-w-0 flex-1 truncate text-[11px] text-[#eff1f666]">
          {breadcrumb}
        </div>

        <div className="shrink-0 lg:hidden">
          <button
            type="button"
            onClick={toggleCode}
            className={cn(
              "inline-flex h-7 items-center gap-1 rounded-md px-2 text-[11px] font-semibold",
              showCode
                ? "bg-[#333] text-white"
                : "bg-[#2cbb5d] text-white",
            )}
          >
            <Code2 className="h-3 w-3" />
            {showCode ? "Close" : "Code"}
          </button>
        </div>
      </div>

      <div className="flex min-h-0 flex-1">
        {showOutline && (
          <aside className="hidden w-[220px] shrink-0 flex-col border-r border-[#333] bg-[#222] lg:flex">
            <div className="min-h-0 flex-1 overflow-hidden">{outline}</div>
            <div className="shrink-0 border-t border-[#333] p-2">
              {interpreterButton}
            </div>
          </aside>
        )}

        <div ref={splitRef} className="flex min-h-0 min-w-0 flex-1">
          <section className="min-h-0 min-w-0 flex-1 overflow-y-auto overscroll-contain bg-[#1e1e1e]">
            <div
              className={cn(
                "mx-auto px-5 py-5 sm:px-8 sm:py-6",
                showCode ? "max-w-3xl" : "max-w-3xl lg:max-w-[48rem]",
              )}
            >
              {content}
            </div>
          </section>

          {showCode && (
            <>
              <div
                role="separator"
                aria-orientation="vertical"
                aria-label="Resize interpreter"
                title="Drag to resize"
                onMouseDown={startResize}
                className="hidden w-1.5 shrink-0 cursor-col-resize bg-[#1a1a1a] hover:bg-[#ffa116]/70 lg:block"
              />
              <aside
                className="flex min-h-[42vh] w-full shrink-0 flex-col overflow-hidden border-t border-[#333] bg-[#1a1a1a] lg:min-h-0 lg:w-[var(--lesson-code-pct)] lg:border-l lg:border-t-0"
                style={
                  {
                    "--lesson-code-pct": `${codePct}%`,
                  } as React.CSSProperties
                }
              >
                <div className="flex h-8 shrink-0 items-center justify-between border-b border-[#333] bg-[#262626] px-2">
                  <span className="text-[11px] font-medium text-[#eff1f6aa]">
                    Interpreter
                  </span>
                  <button
                    type="button"
                    onClick={closeCode}
                    className="inline-flex h-6 items-center gap-1 rounded px-1.5 text-[11px] text-[#eff1f6aa] hover:bg-[#333] hover:text-white"
                  >
                    <PanelRightClose className="h-3.5 w-3.5" />
                    Close
                  </button>
                </div>
                <div className="min-h-0 flex-1">{practice}</div>
              </aside>
            </>
          )}
        </div>
      </div>

      {!showOutline && !showCode && (
        <button
          type="button"
          onClick={openCode}
          className="fixed bottom-4 right-4 z-40 hidden items-center gap-2 rounded-full bg-[#2cbb5d] px-3.5 py-2 text-xs font-semibold text-white shadow-lg hover:bg-[#25a352] lg:inline-flex"
        >
          <Code2 className="h-3.5 w-3.5" />
          Open interpreter
        </button>
      )}

      {mobileOutline && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <button
            type="button"
            className="absolute inset-0 bg-black/60"
            aria-label="Close lessons"
            onClick={() => setMobileOutline(false)}
          />
          <div className="absolute inset-y-0 left-0 flex w-[min(86vw,300px)] flex-col bg-[#222] shadow-xl">
            <div className="flex h-9 items-center justify-between border-b border-[#333] px-3">
              <span className="text-sm font-semibold text-white">Lessons</span>
              <button
                type="button"
                className="rounded p-1 text-[#eff1f6aa] hover:bg-[#333]"
                onClick={() => setMobileOutline(false)}
                aria-label="Close"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="min-h-0 flex-1 overflow-y-auto">{outline}</div>
            <div className="border-t border-[#333] p-2">
              <button
                type="button"
                onClick={() => {
                  setMobileOutline(false);
                  openCode();
                }}
                className="flex w-full items-center justify-center gap-2 rounded-md bg-[#2cbb5d] px-3 py-2 text-xs font-semibold text-white"
              >
                <Code2 className="h-3.5 w-3.5" />
                Open interpreter
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
