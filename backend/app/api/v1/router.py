from fastapi import APIRouter

from app.api.v1.endpoints import auth, chatbot, countries, dashboard, jobs, recommendations, savings, visa

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(countries.router, prefix="/countries", tags=["countries"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(savings.router, prefix="/savings", tags=["savings"])
api_router.include_router(visa.router, prefix="/visa", tags=["visa"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
