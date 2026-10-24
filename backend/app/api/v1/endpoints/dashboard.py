from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.dashboard import country_rankings, executive_dashboard, skills_by_country

router = APIRouter()


@router.get("/executive")
def executive(db: Session = Depends(get_db)):
    return executive_dashboard(db)


@router.get("/rankings")
def rankings(db: Session = Depends(get_db)):
    return {"rankings": country_rankings(db)}


@router.get("/heatmap")
def heatmap(db: Session = Depends(get_db)):
    return {"heatmap": skills_by_country(db)}
