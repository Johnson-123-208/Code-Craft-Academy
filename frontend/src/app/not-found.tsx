import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto flex min-h-[60vh] max-w-lg flex-col items-start justify-center px-4">
      <p className="text-sm font-semibold text-[#ffa116]">404</p>
      <h1 className="mt-2 text-3xl font-semibold text-white">Page not found</h1>
      <p className="mt-3 text-sm text-[#eff1f699]">
        That problem or lesson doesn&apos;t exist — or the URL is mistyped.
      </p>
      <Link
        href="/practice"
        className="mt-8 inline-flex h-10 items-center rounded-lg bg-[#ffa116] px-4 text-sm font-semibold text-[#1a1a1a]"
      >
        Back to Problem List
      </Link>
    </div>
  );
}
