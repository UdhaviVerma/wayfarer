from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.savings import SavingsInput, SavingsOutput
from app.services.calculator import calculate_savings

router = APIRouter()


@router.post("/calculator", response_model=SavingsOutput)
def savings_calculator(payload: SavingsInput, db: Session = Depends(get_db)):
    try:
        data = calculate_savings(db, payload.country, payload.expected_foreign_salary_usd)
        return SavingsOutput(**data)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
