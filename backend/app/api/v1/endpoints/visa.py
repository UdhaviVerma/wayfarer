from fastapi import APIRouter

from app.schemas.visa import VisaRoadmapInput, VisaRoadmapOutput
from app.services.visa import build_visa_roadmap

router = APIRouter()


@router.post("/roadmap", response_model=VisaRoadmapOutput)
def visa_roadmap(payload: VisaRoadmapInput):
    steps = build_visa_roadmap(payload.source_country, payload.target_country)
    return VisaRoadmapOutput(source_country=payload.source_country, target_country=payload.target_country, steps=steps)
