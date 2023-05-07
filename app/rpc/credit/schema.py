"""
@author: igor
"""
from datetime import datetime
from typing import List, Optional, Any, Dict
from uuid import UUID

from pydantic import BaseModel

from app.shared.schemas.orm_schema import ORMCamelModel


class Balance(ORMCamelModel):
    id: UUID
    balance: int
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
