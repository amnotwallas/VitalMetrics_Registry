from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from app.models.goal import GoalType

class GoalCreate(BaseModel):
    type: GoalType
    target_value: float
    unit: str
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None

class GoalRead(BaseModel):
    id: int
    user_id: int
    type: GoalType
    target_value: float
    unit: str
    start_date: datetime
    end_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

