# backend/app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional # Keep Optional if needed for future fields

# --- Task Schemas ---

class TaskBase(BaseModel):
    """
    Base Pydantic model containing common fields for a task.
    Used as a base for creation and response models.
    """
    description: str = Field(..., min_length=1, example="Learn Docker")
    is_completed: bool = Field(default=False, example=False)

class TaskCreate(TaskBase):
    """
    Pydantic model used specifically when creating a new task via the API.
    Inherits fields from TaskBase. Can add creation-specific validation if needed.
    """
    pass # Currently no additional fields needed for creation beyond TaskBase

class TaskUpdate(BaseModel):
    """
    Pydantic model used when updating an existing task via the API.
    All fields are optional, allowing partial updates.
    """
    description: Optional[str] = Field(None, min_length=1, example="Update the documentation")
    is_completed: Optional[bool] = Field(None, example=True)

class TaskResponse(TaskBase):
    """
    Pydantic model used when returning task data in API responses.
    Includes database-generated fields like id and timestamps.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    # Pydantic V2 configuration to enable ORM mode
    # This allows automatic mapping from SQLAlchemy model instances
    model_config = {
        "from_attributes": True
    }

