import "katex/dist/katex.min.css";

export default function LessonsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="h-screen overflow-hidden bg-[#1a1a1a]">{children}</div>
  );
}
