# backend/app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func # To use SQL functions like NOW()
from .database import Base # Import Base from database.py

class Task(Base):
    """
    SQLAlchemy model representing the 'tasks' table in the database.
    """
    __tablename__ = "tasks"

    # Columns definition matching the plan
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=False, index=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    # Use server_default for database-level defaults, ensuring timezone awareness
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # default/onupdate for application-level timestamp handling (updates automatically)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        """Provides a developer-friendly representation of the Task object."""
        return f"<Task(id={self.id}, description='{self.description[:20]}...', completed={self.is_completed})>"

