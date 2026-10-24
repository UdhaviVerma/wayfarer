from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    work_life_balance_score: Mapped[float] = mapped_column(Float, nullable=False)
    visa_difficulty_score: Mapped[float] = mapped_column(Float, nullable=False)
    pr_difficulty_score: Mapped[float] = mapped_column(Float, nullable=False)
    healthcare_score: Mapped[float] = mapped_column(Float, nullable=False)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False)

    salaries = relationship("Salary", back_populates="country")
    taxes = relationship("Tax", back_populates="country")
    living_costs = relationship("CostOfLiving", back_populates="country")
    visa_programs = relationship("VisaProgram", back_populates="country")
    job_markets = relationship("JobMarket", back_populates="country")
    recommendations = relationship("Recommendation", back_populates="country")
