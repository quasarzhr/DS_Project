from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from .database import Base

# Database model for storing task information
class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String, nullable=False)

    assigned_worker_id = Column(Integer, nullable=True)
    result = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)