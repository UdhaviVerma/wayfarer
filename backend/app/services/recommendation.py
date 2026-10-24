from sqlalchemy.orm import Session

from app.models.cost_of_living import CostOfLiving
from app.models.country import Country
from app.models.job_market import JobMarket
from app.models.salary import Salary
from app.models.tax import Tax


def _tech_fit_score(db: Session, country_id: int, tech_stack: str) -> float:
    tech_tokens = [token.strip().lower() for token in tech_stack.split("+")]
    skills = db.query(JobMarket).filter(JobMarket.country_id == country_id).all()
    score = 0.0
    for skill in skills:
        if any(token in skill.skill.lower() for token in tech_tokens):
            score += min(skill.demand_score, 10)
    return min(score, 20.0)


def build_recommendations(db: Session, tech_stack: str, english_level: str) -> list[dict]:
    countries = db.query(Country).all()
    results: list[dict] = []

    english_multiplier = {"basic": 0.8, "intermediate": 1.0, "advanced": 1.1, "fluent": 1.2}.get(
        english_level.lower(), 1.0
    )

    for country in countries:
        salary = db.query(Salary).filter(Salary.country_id == country.id).first()
        tax = db.query(Tax).filter(Tax.country_id == country.id).first()
        col = db.query(CostOfLiving).filter(CostOfLiving.country_id == country.id).first()

        if not salary or not tax or not col:
            continue

        monthly_salary = salary.average_annual_salary_usd / 12
        monthly_tax = monthly_salary * (tax.effective_tax_percent / 100)
        monthly_expenses = col.rent_usd + col.living_expenses_usd + col.transport_usd
        monthly_savings = monthly_salary - monthly_tax - monthly_expenses

        composite = (
            (salary.average_annual_salary_usd / 3000) * 0.25
            + max(monthly_savings / 400, 0) * 0.25
            + (10 - country.pr_difficulty_score) * 0.15
            + country.work_life_balance_score * 0.15
            + country.healthcare_score * 0.1
            + country.safety_score * 0.1
        )

        composite += _tech_fit_score(db, country.id, tech_stack) * 0.05
        composite *= english_multiplier

        risk = "Low"
        if country.visa_difficulty_score >= 7 or country.pr_difficulty_score >= 7:
            risk = "Medium"
        if country.visa_difficulty_score >= 8.5 or country.pr_difficulty_score >= 8.5:
            risk = "High"

        reasoning = (
            f"{country.name} scores high due to salary (${salary.average_annual_salary_usd:,.0f}), "
            f"estimated monthly savings (${monthly_savings:,.0f}), and PR difficulty "
            f"({country.pr_difficulty_score}/10)."
        )

        results.append(
            {
                "country": country.name,
                "score": round(composite, 2),
                "best_salary": salary.average_annual_salary_usd,
                "best_savings": round(monthly_savings, 2),
                "fastest_pr": round(10 - country.pr_difficulty_score, 2),
                "work_life_balance": country.work_life_balance_score,
                "risk_assessment": risk,
                "reasoning": reasoning,
            }
        )

    return sorted(results, key=lambda row: row["score"], reverse=True)
