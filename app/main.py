from fastapi import FastAPI
from sqlmodel import SQLModel

from app.api.v1.router import api_router
from app.db.session import engine
from app.core.config import settings

def create_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Vital Metrics Registry API",
    description="A backend-first API for a digital health dashboard.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Vital Metrics Registry API"}
