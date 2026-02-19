from sqlmodel import SQLModel
# Import all models here so that they are registered with SQLModel
from app.models.metric import Metric, User, Goal
