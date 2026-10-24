from pydantic import BaseModel


class VisaRoadmapInput(BaseModel):
    source_country: str
    target_country: str


class VisaRoadmapOutput(BaseModel):
    source_country: str
    target_country: str
    steps: list[str]
