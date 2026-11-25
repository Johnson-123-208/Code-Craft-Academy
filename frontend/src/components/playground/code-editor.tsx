"use client";

import { useRef } from "react";
import Editor, { loader, type OnMount } from "@monaco-editor/react";

// Load Monaco from CDN so Next doesn't bundle the full editor into every page
loader.config({
  paths: {
    vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/min/vs",
  },
});

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  height?: string;
  readOnly?: boolean;
  onRun?: () => void;
  onSubmit?: () => void;
}

export function CodeEditor({
  value,
  onChange,
  height = "100%",
  readOnly = false,
  onRun,
  onSubmit,
}: CodeEditorProps) {
  const runRef = useRef(onRun);
  const submitRef = useRef(onSubmit);
  runRef.current = onRun;
  submitRef.current = onSubmit;

  const handleMount: OnMount = (ed, monaco) => {
    ed.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
      runRef.current?.();
    });
    ed.addCommand(
      monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter,
      () => {
        submitRef.current?.();
      },
    );

    ed.updateOptions({
      quickSuggestions: { other: true, comments: false, strings: false },
      suggestOnTriggerCharacters: true,
      acceptSuggestionOnEnter: "on",
      tabCompletion: "on",
      autoClosingBrackets: "languageDefined",
      autoClosingQuotes: "languageDefined",
      formatOnPaste: true,
      multiCursorModifier: "ctrlCmd",
    });

    ed.focus();
  };

  return (
    <Editor
      height={height}
      defaultLanguage="python"
      theme="vs-dark"
      value={value}
      onChange={(v) => onChange(v ?? "")}
      loading={
        <div className="flex h-full items-center justify-center bg-[#1e1e1e] text-xs text-[#eff1f666]">
          Loading editor…
        </div>
      }
      options={{
        readOnly,
        minimap: { enabled: false },
        fontSize: 14,
        fontFamily:
          "var(--font-mono), 'IBM Plex Mono', ui-monospace, Menlo, Monaco, monospace",
        fontLigatures: false,
        lineHeight: 22,
        scrollBeyondLastLine: false,
        automaticLayout: true,
        tabSize: 4,
        insertSpaces: true,
        detectIndentation: false,
        wordWrap: "on",
        padding: { top: 12, bottom: 12 },
        renderLineHighlight: "line",
        cursorBlinking: "smooth",
        cursorSmoothCaretAnimation: "on",
        smoothScrolling: true,
        scrollbar: {
          verticalScrollbarSize: 8,
          horizontalScrollbarSize: 8,
          useShadows: false,
        },
        overviewRulerLanes: 0,
        hideCursorInOverviewRuler: true,
        folding: true,
        glyphMargin: false,
        lineNumbersMinChars: 3,
        renderWhitespace: "selection",
        links: false,
        colorDecorators: false,
      }}
      onMount={handleMount}
    />
  );
}
