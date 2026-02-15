from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from datetime import datetime, timedelta

from app.schemas.metric import MetricCreate, MetricRead, KPIResponse
from app.repository import metric_repository
from app.services import kpi_service
from app.db.session import get_db
from app.models.metric import User
from app.security import get_current_active_user
from typing import Optional

router = APIRouter()

@router.post("/", response_model=MetricRead, status_code=201)
def create_metric(
    *,
    db: Session = Depends(get_db),
    metric_in: MetricCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Ingest a new raw biometric data point.
    """
    metric = metric_repository.create_with_owner(
        db=db, obj_in=metric_in, user_id=current_user.id
    )
    return metric

@router.get("/", response_model=List[MetricRead])
def read_metrics(
    *,
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve raw metric records for the current user within a date range.
    """
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=7)
    if not end_date:
        end_date = datetime.utcnow()
        
    metrics = metric_repository.get_multi_by_owner(
        db=db, user_id=current_user.id, start_date=start_date, end_date=end_date
    )
    return metrics

@router.get("/kpis", response_model=KPIResponse)
def get_kpis(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Compute and return daily KPIs for the current user.
    KPIs are derived on-the-fly from raw data.
    """
    # set  example goals (feat: implemtent user-specific goals in the future in database)
    goals = {"steps": 10000, "calories": 2500, "sleep": 8}
    
    kpis = kpi_service.calculate_daily_kpis(
        db=db, user_id=current_user.id, goals=goals
    )
    return kpis
