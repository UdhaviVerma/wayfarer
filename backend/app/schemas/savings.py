from pydantic import BaseModel, Field


class SavingsInput(BaseModel):
    country: str
    current_salary_lpa: float = Field(ge=1)
    expected_foreign_salary_usd: float = Field(ge=1000)


class SavingsOutput(BaseModel):
    monthly_tax_usd: float
    monthly_rent_usd: float
    monthly_living_usd: float
    monthly_transport_usd: float
    monthly_savings_usd: float
    yearly_savings_usd: float
    savings_percentage: float
