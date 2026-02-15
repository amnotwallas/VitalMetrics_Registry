import enum
from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel


class MetricType(str, enum.Enum):
    steps = "steps"
    calories = "calories"
    sleep = "sleep"
    heart_rate = "heart_rate"


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    metrics: List["Metric"] = Relationship(back_populates="user")


class MetricBase(SQLModel):
    type: MetricType = Field(index=True)
    value: float
    unit: str
    timestamp: datetime = Field(index=True)


class Metric(MetricBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    user: User = Relationship(back_populates="metrics")

