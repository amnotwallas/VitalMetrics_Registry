from datetime import datetime
from typing import List
from sqlmodel import Session, select

from app.models.goal import Goal
from app.schemas.goal import GoalCreate

def create_with_owner(db: Session, *, obj_in: GoalCreate, user_id: int) -> Goal:
    db_obj = Goal(**obj_in.dict(), user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_multi_by_owner(
    db: Session, *, user_id: int, start_date: datetime, end_date: datetime
) -> List[Goal]:
    statement = (
        select(Goal)
        .where(Goal.user_id == user_id)
        .where(Goal.start_date >= start_date)
        .where(Goal.end_date <= end_date)
        .order_by(Goal.start_date.desc())
    )
    return db.exec(statement).all()

def get_active_by_owner(db: Session, *, user_id: int, current_date: datetime) -> List[Goal]:
    statement = (
        select(Goal)
        .where(Goal.user_id == user_id)
        .where(Goal.start_date <= current_date)
        .where((Goal.end_date >= current_date) | (Goal.end_date == None))
        .order_by(Goal.start_date.desc())
    )
    return db.exec(statement).all()

def get_active_goals_by_user(db: Session, *, user_id: int) -> List[Goal]:
    current_date = datetime.utcnow()
    return get_active_by_owner(db=db, user_id=user_id, current_date=current_date)

def get(db: Session, id: int) -> Goal:
    return db.get(Goal, id)