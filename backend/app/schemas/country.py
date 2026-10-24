from pydantic import BaseModel


class CountryComparison(BaseModel):
    country: str
    average_salary_usd: float
    tax_percent: float
    rent_usd: float
    cost_of_living_usd: float
    transport_usd: float
    monthly_expenses_usd: float
    average_savings_usd: float
    work_life_balance_score: float
    visa_difficulty_score: float
    pr_difficulty_score: float
    healthcare_score: float
    safety_score: float
