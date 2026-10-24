const posts = [
  "Germany vs Canada: Where can Java developers save more?",
  "Top 5 countries for DevOps engineers in 2026",
  "How to plan PR strategy before accepting an offer",
];

export default function BlogPage() {
  return (
    <main className="space-y-6">
      <h1 className="text-3xl font-bold">Blog</h1>
      <ul className="space-y-3">
        {posts.map((title) => (
          <li key={title} className="rounded-2xl border border-border p-4 text-sm">
            {title}
          </li>
        ))}
      </ul>
    </main>
  );
}
