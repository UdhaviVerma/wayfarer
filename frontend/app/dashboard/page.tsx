"use client";

import { useEffect, useMemo, useState } from "react";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { apiGet, apiPost } from "@/lib/api";

type CountryRow = {
  country: string;
  average_salary_usd: number;
  tax_percent: number;
  rent_usd: number;
  cost_of_living_usd: number;
  transport_usd: number;
  monthly_expenses_usd: number;
  average_savings_usd: number;
  work_life_balance_score: number;
  visa_difficulty_score: number;
  pr_difficulty_score: number;
  healthcare_score: number;
  safety_score: number;
};

type RecRow = {
  country: string;
  score: number;
  best_salary: number;
  best_savings: number;
  fastest_pr: number;
  work_life_balance: number;
  risk_assessment: string;
  reasoning: string;
};

export default function DashboardPage() {
  const [countries, setCountries] = useState<CountryRow[]>([]);
  const [search, setSearch] = useState("");
  const [skills, setSkills] = useState<{ country: string; skill: string; demand_score: number }[]>([]);
  const [roadmap, setRoadmap] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<RecRow[]>([]);
  const [chatReply, setChatReply] = useState("");
  const [savings, setSavings] = useState<{ name: string; value: number }[]>([]);
  const [advisorPayload, setAdvisorPayload] = useState<null | {
    age: number;
    experience_years: number;
    current_salary_lpa: number;
    tech_stack: string;
    english_level: string;
  }>(null);

  useEffect(() => {
    apiGet<CountryRow[]>('/countries/compare').then(setCountries).catch(console.error);
    apiGet<{ skills: { country: string; skill: string; demand_score: number }[] }>('/jobs/market')
      .then((r) => setSkills(r.skills))
      .catch(console.error);
  }, []);

  const filtered = useMemo(
    () => countries.filter((item) => item.country.toLowerCase().includes(search.toLowerCase())),
    [countries, search],
  );

  const heatMapRows = useMemo(() => {
    const grouped: Record<string, number> = {};
    skills.forEach((s) => {
      grouped[s.country] = Math.max(grouped[s.country] ?? 0, s.demand_score);
    });
    return Object.entries(grouped).map(([country, demand]) => ({ country, demand }));
  }, [skills]);

  async function handleRecommendations(formData: FormData) {
    const payload = {
      age: Number(formData.get("age")),
      experience_years: Number(formData.get("experience")),
      current_salary_lpa: Number(formData.get("salary")),
      tech_stack: String(formData.get("stack")),
      english_level: String(formData.get("english")),
    };
    const response = await apiPost<{ top_5: RecRow[] }>('/recommendations/advisor', payload);
    setAdvisorPayload(payload);
    setRecommendations(response.top_5);
  }

  async function downloadReport() {
    if (!advisorPayload) return;
    const base =
      process.env.NEXT_PUBLIC_API_URL ||
      (process.env.NODE_ENV === 'production'
        ? 'https://wayfarer-backend-ai.onrender.com/api/v1'
        : 'http://localhost:8000/api/v1');
    const response = await fetch(`${base}/recommendations/report`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(advisorPayload),
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'relocation-report.pdf';
    link.click();
    URL.revokeObjectURL(url);
  }

  async function handleSavings(formData: FormData) {
    const payload = {
      country: String(formData.get("country")),
      current_salary_lpa: Number(formData.get("current_salary")),
      expected_foreign_salary_usd: Number(formData.get("expected_salary")),
    };
    const response = await apiPost<{
      monthly_tax_usd: number;
      monthly_rent_usd: number;
      monthly_living_usd: number;
      monthly_transport_usd: number;
      monthly_savings_usd: number;
      yearly_savings_usd: number;
    }>('/savings/calculator', payload);

    setSavings([
      { name: "Tax", value: response.monthly_tax_usd },
      { name: "Rent", value: response.monthly_rent_usd },
      { name: "Living", value: response.monthly_living_usd },
      { name: "Transport", value: response.monthly_transport_usd },
      { name: "Savings", value: response.monthly_savings_usd },
    ]);
  }

  async function handleVisa(formData: FormData) {
    const payload = {
      source_country: String(formData.get("source")),
      target_country: String(formData.get("target")),
    };
    const response = await apiPost<{ steps: string[] }>('/visa/roadmap', payload);
    setRoadmap(response.steps);
  }

  async function handleChat(formData: FormData) {
    const payload = { message: String(formData.get("message")) };
    const response = await apiPost<{ response: string }>('/chatbot/query', payload);
    setChatReply(response.response);
  }

  return (
    <main className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      <Card>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Country Comparison</h2>
          <Input placeholder="Search country" value={search} onChange={(e) => setSearch(e.target.value)} className="max-w-xs" />
        </div>
        <div className="overflow-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="p-2">Country</th><th className="p-2">Salary</th><th className="p-2">Tax%</th><th className="p-2">Savings/mo</th><th className="p-2">WLB</th><th className="p-2">PR</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row) => (
                <tr key={row.country} className="border-b border-border/70">
                  <td className="p-2">{row.country}</td>
                  <td className="p-2">${row.average_salary_usd.toLocaleString()}</td>
                  <td className="p-2">{row.tax_percent}</td>
                  <td className="p-2">${row.average_savings_usd.toLocaleString()}</td>
                  <td className="p-2">{row.work_life_balance_score}</td>
                  <td className="p-2">{row.pr_difficulty_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <h2 className="mb-3 text-lg font-semibold">AI Relocation Advisor</h2>
          <form
            className="space-y-2"
            onSubmit={(e) => {
              e.preventDefault();
              handleRecommendations(new FormData(e.currentTarget));
            }}
          >
            <Input name="age" placeholder="Age" />
            <Input name="experience" placeholder="Experience (years)" />
            <Input name="salary" placeholder="Current salary LPA" />
            <Input name="stack" placeholder="Tech stack (e.g. Java + Spring Boot)" />
            <Input name="english" placeholder="English level" />
            <Button type="submit">Get Top 5 Countries</Button>
          </form>
          <div className="mt-3 space-y-2 text-sm">
            {recommendations.length > 0 && (
              <Button variant="outline" onClick={downloadReport}>Download PDF Report</Button>
            )}
            {recommendations.map((r) => (
              <div key={r.country} className="rounded-xl border border-border p-2">
                <p className="font-medium">{r.country} • Score {r.score} • Risk {r.risk_assessment}</p>
                <p className="opacity-80">{r.reasoning}</p>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <h2 className="mb-3 text-lg font-semibold">Savings Calculator</h2>
          <form
            className="space-y-2"
            onSubmit={(e) => {
              e.preventDefault();
              handleSavings(new FormData(e.currentTarget));
            }}
          >
            <Input name="country" placeholder="Country" />
            <Input name="current_salary" placeholder="Current salary LPA" />
            <Input name="expected_salary" placeholder="Expected salary USD/year" />
            <Button type="submit">Calculate Savings</Button>
          </form>
          <div className="mt-4 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={savings}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="hsl(var(--primary))" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <h2 className="mb-3 text-lg font-semibold">Visa Roadmap Timeline</h2>
          <form
            className="mb-3 flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              handleVisa(new FormData(e.currentTarget));
            }}
          >
            <Input name="source" placeholder="Source country" defaultValue="India" />
            <Input name="target" placeholder="Target country" defaultValue="Germany" />
            <Button type="submit">Generate</Button>
          </form>
          <ol className="space-y-2 text-sm">
            {roadmap.map((step) => (
              <li key={step} className="rounded-xl border border-border p-2">{step}</li>
            ))}
          </ol>
        </Card>

        <Card>
          <h2 className="mb-3 text-lg font-semibold">Job Market Analysis</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={heatMapRows}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="country" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="demand" stroke="hsl(var(--primary))" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <Card>
        <h2 className="mb-3 text-lg font-semibold">AI Chatbot</h2>
        <form
          className="flex gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            handleChat(new FormData(e.currentTarget));
          }}
        >
          <Input name="message" placeholder="Should I move to Germany or UAE?" />
          <Button type="submit">Ask</Button>
        </form>
        {chatReply && <p className="mt-3 rounded-xl border border-border p-3 text-sm">{chatReply}</p>}
      </Card>
    </main>
  );
}
