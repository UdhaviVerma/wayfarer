from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.cost_of_living import CostOfLiving
from app.models.country import Country
from app.models.job_market import JobMarket
from app.models.salary import Salary
from app.models.tax import Tax


def executive_dashboard(db: Session) -> dict:
    total_countries = db.query(func.count(Country.id)).scalar() or 0
    avg_salary = db.query(func.avg(Salary.average_annual_salary_usd)).scalar() or 0
    avg_tax = db.query(func.avg(Tax.effective_tax_percent)).scalar() or 0

    return {
        "total_countries": total_countries,
        "average_salary_usd": round(float(avg_salary), 2),
        "average_tax_percent": round(float(avg_tax), 2),
    }


def country_rankings(db: Session) -> list[dict]:
    countries = db.query(Country).all()
    rows: list[dict] = []
    for country in countries:
        sal = db.query(Salary).filter(Salary.country_id == country.id).first()
        tax = db.query(Tax).filter(Tax.country_id == country.id).first()
        col = db.query(CostOfLiving).filter(CostOfLiving.country_id == country.id).first()
        if not sal or not tax or not col:
            continue
        monthly = sal.average_annual_salary_usd / 12
        savings = monthly - (monthly * tax.effective_tax_percent / 100) - col.rent_usd - col.living_expenses_usd - col.transport_usd
        rows.append({"country": country.name, "estimated_monthly_savings": round(savings, 2)})
    return sorted(rows, key=lambda item: item["estimated_monthly_savings"], reverse=True)


def skills_by_country(db: Session) -> list[dict]:
    rows = db.query(Country.name, JobMarket.skill, JobMarket.demand_score).join(JobMarket).all()
    return [{"country": country, "skill": skill, "demand_score": demand} for country, skill, demand in rows]
