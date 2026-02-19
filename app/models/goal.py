import enum
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User

class GoalType(str, enum.Enum):
    steps = "steps"
    calories = "calories"
    sleep = "sleep"
    heart_rate = "heart_rate"

class Goal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: GoalType = Field(index=True)
    target_value: float
    unit: str
    start_date: Optional[datetime] = Field(index=True)
    end_date: Optional[datetime] = Field(index=True)

    user_id: int = Field(foreign_key="user.id", index=True)
    user: "User" = Relationship(back_populates="goals")