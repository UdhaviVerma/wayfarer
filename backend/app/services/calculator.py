from sqlalchemy.orm import Session

from app.models.cost_of_living import CostOfLiving
from app.models.country import Country
from app.models.tax import Tax


def calculate_savings(db: Session, country_name: str, annual_salary_usd: float) -> dict[str, float]:
    country = db.query(Country).filter(Country.name == country_name).first()
    if not country:
        raise ValueError("Country not found")

    tax = db.query(Tax).filter(Tax.country_id == country.id).first()
    col = db.query(CostOfLiving).filter(CostOfLiving.country_id == country.id).first()

    if not tax or not col:
        raise ValueError("Country financial profile incomplete")

    monthly_salary = annual_salary_usd / 12
    monthly_tax = monthly_salary * (tax.effective_tax_percent / 100)
    monthly_rent = col.rent_usd
    monthly_living = col.living_expenses_usd
    monthly_transport = col.transport_usd

    monthly_savings = monthly_salary - monthly_tax - monthly_rent - monthly_living - monthly_transport
    yearly_savings = monthly_savings * 12
    savings_percentage = (monthly_savings / monthly_salary) * 100 if monthly_salary else 0

    return {
        "monthly_tax_usd": round(monthly_tax, 2),
        "monthly_rent_usd": round(monthly_rent, 2),
        "monthly_living_usd": round(monthly_living, 2),
        "monthly_transport_usd": round(monthly_transport, 2),
        "monthly_savings_usd": round(monthly_savings, 2),
        "yearly_savings_usd": round(yearly_savings, 2),
        "savings_percentage": round(savings_percentage, 2),
    }
