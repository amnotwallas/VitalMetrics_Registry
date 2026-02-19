from fastapi import APIRouter
from app.api.v1.endpoints import metrics, auth, goals

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
