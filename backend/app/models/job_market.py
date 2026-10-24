from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class JobMarket(Base):
    __tablename__ = "job_market"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    skill: Mapped[str] = mapped_column(String(120), nullable=False)
    demand_score: Mapped[int] = mapped_column(Integer, nullable=False)

    country = relationship("Country", back_populates="job_markets")
