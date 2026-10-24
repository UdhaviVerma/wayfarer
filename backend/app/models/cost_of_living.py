from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CostOfLiving(Base):
    __tablename__ = "cost_of_living"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    rent_usd: Mapped[float] = mapped_column(Float, nullable=False)
    living_expenses_usd: Mapped[float] = mapped_column(Float, nullable=False)
    transport_usd: Mapped[float] = mapped_column(Float, nullable=False)

    country = relationship("Country", back_populates="living_costs")
