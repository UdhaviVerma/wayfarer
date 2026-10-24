import { Card } from "@/components/ui/card";

const tiers = [
  { name: "Starter", price: "Free", details: "Country comparison + savings calculator" },
  { name: "Pro", price: "$19/mo", details: "AI advisor + visa roadmap + chat" },
  { name: "Career Plus", price: "$49/mo", details: "PDF reports + strategy plans + priority support" },
];

export default function PricingPage() {
  return (
    <main className="space-y-6">
      <h1 className="text-3xl font-bold">Pricing</h1>
      <div className="grid gap-4 md:grid-cols-3">
        {tiers.map((tier) => (
          <Card key={tier.name}>
            <p className="text-sm opacity-70">{tier.name}</p>
            <p className="mt-2 text-2xl font-semibold">{tier.price}</p>
            <p className="mt-2 text-sm">{tier.details}</p>
          </Card>
        ))}
      </div>
    </main>
  );
}
