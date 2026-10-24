from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.dashboard import skills_by_country

router = APIRouter()


@router.get("/market")
def job_market(db: Session = Depends(get_db)):
    return {"skills": skills_by_country(db)}
