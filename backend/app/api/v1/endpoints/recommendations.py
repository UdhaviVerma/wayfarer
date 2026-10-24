from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.recommendation import RecommendationInput, RecommendationResponse
from app.services.recommendation import build_recommendations

router = APIRouter()


@router.post("/advisor", response_model=RecommendationResponse)
def advisor(payload: RecommendationInput, db: Session = Depends(get_db)):
    ranked = build_recommendations(db, payload.tech_stack, payload.english_level)
    top_five = ranked[:5]
    if not top_five:
        raise HTTPException(status_code=404, detail="No recommendations available")
    return {"top_5": top_five, "best_overall": top_five[0]}


@router.post("/report")
def recommendation_report(payload: RecommendationInput, db: Session = Depends(get_db)):
    ranked = build_recommendations(db, payload.tech_stack, payload.english_level)[:5]
    if not ranked:
        raise HTTPException(status_code=404, detail="No recommendations available")

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    y = 800
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Global Developer Relocation Advisor Report")
    y -= 30
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, f"Profile: {payload.experience_years} years | Stack: {payload.tech_stack} | English: {payload.english_level}")
    y -= 25

    for idx, row in enumerate(ranked, start=1):
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(40, y, f"{idx}. {row['country']} (Score: {row['score']})")
        y -= 16
        pdf.setFont("Helvetica", 9)
        pdf.drawString(52, y, f"Salary: ${row['best_salary']:,.0f} | Monthly Savings: ${row['best_savings']:,.0f} | Risk: {row['risk_assessment']}")
        y -= 14
        pdf.drawString(52, y, row["reasoning"][:110])
        y -= 20
        if y < 80:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=relocation-report.pdf"},
    )
