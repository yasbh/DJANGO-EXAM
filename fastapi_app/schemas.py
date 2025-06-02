# fastapi_app/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

class TaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = ""
    status: Optional[str] = "PENDING"

class TaskResponse(BaseModel):
    task_id: int
    message: str
