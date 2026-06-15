from pydantic import BaseModel
from typing import Optional

from app.models import Users

class DepartmentCreate(BaseModel):
    name: str
    responsible_id: int
    creator: Users
    company_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True