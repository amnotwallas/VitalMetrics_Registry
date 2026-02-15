from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from app.models.metric import MetricType


# --- Schemas for Raw Metric Ingestion & Querying ---

class MetricCreate(BaseModel):
    type: MetricType
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MetricRead(BaseModel):
    id: int
    user_id: int
    type: MetricType
    value: float
    unit: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


# --- Schemas for Derived KPI Responses (Output ONLY) ---

class KPIValue(BaseModel):
    value: float
    goal: Optional[float] = None


class KPIResponse(BaseModel):
    steps: Optional[KPIValue] = None
    calories: Optional[KPIValue] = None
    sleep: Optional[KPIValue] = None
    heart_rate: Optional[KPIValue] = None

