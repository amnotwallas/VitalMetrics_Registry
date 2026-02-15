from datetime import datetime, timedelta
from typing import Dict, List
from sqlmodel import Session

from app.models.metric import Metric, MetricType
from app.schemas.metric import KPIResponse, KPIValue
from app.repository import metric_repository

def calculate_daily_kpis(db: Session, *, user_id: int, goals: Dict[str, float]) -> KPIResponse:
    """
    Calculates the Key Performance Indicators (KPIs) for the last 24 hours.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=1)

    raw_metrics = metric_repository.get_multi_by_owner(
        db=db, user_id=user_id, start_date=start_date, end_date=end_date
    )

    # Process metrics into a dictionary for easy access
    processed: Dict[MetricType, List[float]] = {mtype: [] for mtype in MetricType}
    for metric in raw_metrics:
        processed[metric.type].append(metric.value)

    # Calculate aggregated values
    steps = sum(processed[MetricType.steps])
    calories = sum(processed[MetricType.calories])
    sleep = sum(processed[MetricType.sleep])
    
    heart_rate_values = processed[MetricType.heart_rate]
    avg_heart_rate = sum(heart_rate_values) / len(heart_rate_values) if heart_rate_values else 0

    # Build response model
    kpis = KPIResponse(
        steps=KPIValue(value=steps, goal=goals.get("steps")),
        calories=KPIValue(value=calories, goal=goals.get("calories")),
        sleep=KPIValue(value=sleep, goal=goals.get("sleep")),
        heart_rate=KPIValue(value=avg_heart_rate) if avg_heart_rate > 0 else None,
    )
    return kpis
