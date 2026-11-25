import "katex/dist/katex.min.css";

export default function PracticeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <div className="lc-practice-shell -mt-0">{children}</div>;
}
