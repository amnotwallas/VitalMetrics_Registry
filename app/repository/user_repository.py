from typing import Optional
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.user import UserCreate
from app.security import get_password_hash

def get_user_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.exec(select(User).where(User.email == email)).first()

def create_user(db: Session, *, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_obj = User(email=user_in.email, hashed_password=hashed_password)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
