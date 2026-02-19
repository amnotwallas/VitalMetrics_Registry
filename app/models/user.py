from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.metric import Metric

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    metrics: List["Metric"] = Relationship(back_populates="user")
    goals: List["Goal"] = Relationship(back_populates="user")
