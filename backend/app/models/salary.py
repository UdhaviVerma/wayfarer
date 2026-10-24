from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Salary(Base):
    __tablename__ = "salaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[str] = mapped_column(String(120), nullable=False)
    average_annual_salary_usd: Mapped[float] = mapped_column(Float, nullable=False)

    country = relationship("Country", back_populates="salaries")
