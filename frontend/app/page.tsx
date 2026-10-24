import Link from "next/link";

import { Card } from "@/components/ui/card";

const highlights = [
  "Compare 10 countries on salary, tax, savings, PR, healthcare, and safety",
  "Get AI relocation recommendations personalized to your profile",
  "Visualize savings and job market trends with interactive charts",
];

export default function HomePage() {
  return (
    <main className="space-y-8">
      <section className="rounded-3xl border border-border p-10">
        <p className="mb-3 text-sm text-blue-500">2026 Developer Relocation Intelligence</p>
        <h1 className="mb-3 text-4xl font-bold leading-tight">Global Developer Relocation Advisor</h1>
        <p className="max-w-2xl text-sm opacity-80">
          Decide where to move with data-driven country comparisons, AI recommendations, visa roadmaps,
          and savings forecasts designed for software engineers from India.
        </p>
        <div className="mt-6 flex gap-3">
          <Link href="/dashboard" className="rounded-xl bg-primary px-4 py-2 text-sm font-medium text-white">Open Dashboard</Link>
          <Link href="/pricing" className="rounded-xl border border-border px-4 py-2 text-sm">View Pricing</Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {highlights.map((item) => (
          <Card key={item}>
            <p className="text-sm">{item}</p>
          </Card>
        ))}
      </section>
    </main>
  );
}
