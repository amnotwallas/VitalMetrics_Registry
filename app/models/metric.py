import enum
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.goal import Goal 
    from app.models.user import User

class MetricType(str, enum.Enum):
    steps = "steps"
    calories = "calories"
    sleep = "sleep"
    heart_rate = "heart_rate"

class Metric(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: MetricType = Field(index=True)
    value: float
    unit: str
    timestamp: datetime = Field(index=True)
    
    user_id: int = Field(foreign_key="user.id", index=True)
    user: "User" = Relationship(back_populates="metrics")