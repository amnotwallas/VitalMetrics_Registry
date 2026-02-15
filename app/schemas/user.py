from typing import Optional
from sqlmodel import SQLModel, Field

class UserCreate(SQLModel):
    email: str
    password: str = Field(..., min_length=8, max_length=72)

class UserRead(SQLModel):
    id: int
    email: str
    is_active: bool
