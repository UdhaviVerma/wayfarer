const faqs = [
  {
    q: "How accurate are salary and savings estimates?",
    a: "Figures are benchmark estimates based on seeded market datasets and should be validated against live offers.",
  },
  {
    q: "Can I compare Germany vs UAE directly?",
    a: "Yes, the comparison dashboard supports country-level salary, tax, and net savings contrasts.",
  },
  {
    q: "Does the app include PR analysis?",
    a: "Yes, recommendations include PR difficulty and a migration pathway.",
  },
];

export default function FAQPage() {
  return (
    <main className="space-y-6">
      <h1 className="text-3xl font-bold">FAQ</h1>
      <div className="space-y-4">
        {faqs.map((item) => (
          <div key={item.q} className="rounded-2xl border border-border p-4">
            <p className="font-medium">{item.q}</p>
            <p className="mt-1 text-sm opacity-80">{item.a}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
