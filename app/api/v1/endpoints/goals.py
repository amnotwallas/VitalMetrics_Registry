from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from datetime import datetime, timedelta

from app.schemas.goal import GoalCreate, GoalRead
from app.repository import goal_repository
from app.db.session import get_db
from app.models.user import User
from app.security import get_current_active_user
from typing import Optional

router = APIRouter()


@router.post("/goals", response_model=GoalRead, status_code=201)
def create_goal(
    *,
    db: Session = Depends(get_db),
    goal_in: GoalCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new health goal for the current user.
    """
    goal = goal_repository.create_with_owner(
        db=db, obj_in=goal_in, user_id=current_user.id
    )
    return goal

@router.get("/goals", response_model=List[GoalRead])
def read_goals(
    *,
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve health goals for the current user within a date range.
    If no date range is provided, defaults to goals from the past month.
    """
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()
        
    goals_list = goal_repository.get_active_goals_by_user(db=db, user_id=current_user.id)
    return goals_list