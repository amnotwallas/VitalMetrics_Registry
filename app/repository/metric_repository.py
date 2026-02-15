from datetime import datetime
from typing import List
from sqlmodel import Session, select

from app.models.metric import Metric
from app.schemas.metric import MetricCreate

def create_with_owner(db: Session, *, obj_in: MetricCreate, user_id: int) -> Metric:
    db_obj = Metric(**obj_in.dict(), user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_multi_by_owner(
    db: Session, *, user_id: int, start_date: datetime, end_date: datetime
) -> List[Metric]:
    statement = (
        select(Metric)
        .where(Metric.user_id == user_id)
        .where(Metric.timestamp >= start_date)
        .where(Metric.timestamp <= end_date)
        .order_by(Metric.timestamp.desc())
    )
    return db.exec(statement).all()
