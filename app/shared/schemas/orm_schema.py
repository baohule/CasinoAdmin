"""
@author: Kuro
"""
from typing import Dict, Any

from fastapi_camelcase import CamelModel


class Schema(CamelModel):
    __abstract__ = True
    fields: Dict[str, Any] = {}


class ORMSchema(Schema):
    class Config:
        orm_mode = True
