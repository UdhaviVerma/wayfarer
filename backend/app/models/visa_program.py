from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class VisaProgram(Base):
    __tablename__ = "visa_programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    visa_name: Mapped[str] = mapped_column(String(120), nullable=False)
    pathway_summary: Mapped[str] = mapped_column(Text, nullable=False)
    processing_time_months: Mapped[int] = mapped_column(Integer, nullable=False)

    country = relationship("Country", back_populates="visa_programs")
