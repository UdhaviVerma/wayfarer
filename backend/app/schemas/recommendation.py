from pydantic import BaseModel, Field


class RecommendationInput(BaseModel):
    age: int = Field(ge=18, le=60)
    experience_years: float = Field(ge=0, le=40)
    current_salary_lpa: float = Field(ge=1)
    tech_stack: str
    english_level: str


class RankedCountry(BaseModel):
    country: str
    score: float
    best_salary: float
    best_savings: float
    fastest_pr: float
    work_life_balance: float
    risk_assessment: str
    reasoning: str


class RecommendationResponse(BaseModel):
    top_5: list[RankedCountry]
    best_overall: RankedCountry
