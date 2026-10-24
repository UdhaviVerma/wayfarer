from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.cost_of_living import CostOfLiving
from app.models.country import Country
from app.models.salary import Salary
from app.models.tax import Tax
from app.schemas.country import CountryComparison

router = APIRouter()


@router.get("/compare", response_model=list[CountryComparison])
def compare_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    rows: list[CountryComparison] = []

    for country in countries:
        salary = db.query(Salary).filter(Salary.country_id == country.id).first()
        tax = db.query(Tax).filter(Tax.country_id == country.id).first()
        col = db.query(CostOfLiving).filter(CostOfLiving.country_id == country.id).first()

        if not salary or not tax or not col:
            continue

        monthly_salary = salary.average_annual_salary_usd / 12
        monthly_tax = monthly_salary * (tax.effective_tax_percent / 100)
        monthly_expenses = col.rent_usd + col.living_expenses_usd + col.transport_usd
        savings = monthly_salary - monthly_tax - monthly_expenses

        rows.append(
            CountryComparison(
                country=country.name,
                average_salary_usd=salary.average_annual_salary_usd,
                tax_percent=tax.effective_tax_percent,
                rent_usd=col.rent_usd,
                cost_of_living_usd=col.living_expenses_usd,
                transport_usd=col.transport_usd,
                monthly_expenses_usd=round(monthly_expenses, 2),
                average_savings_usd=round(savings, 2),
                work_life_balance_score=country.work_life_balance_score,
                visa_difficulty_score=country.visa_difficulty_score,
                pr_difficulty_score=country.pr_difficulty_score,
                healthcare_score=country.healthcare_score,
                safety_score=country.safety_score,
            )
        )

    return rows
