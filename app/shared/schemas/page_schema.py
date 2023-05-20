"""
@author: Kuro
"""
from fastapi.types import Any
from app.shared.schemas.orm_schema import Schema
from typing import List, Optional, Dict
from uuid import UUID

from app.shared.schemas.orm_schema import ORMSchema, Schema


class Params(Schema):
    page: int
    size: int

    class Config:
        schema_extra = {"example": {"page": "1", "size": "10"}}


class Filter(Schema):
    filter: Optional[Dict[str, UUID]]


class Post(Schema):
    post_id: UUID


class GetOptionalContextPages(Schema):
    context: Optional[Filter]
    params: Params


class GetNoContextPages(Schema):
    params: Params


class GetPages(Schema):
    context: Filter
    params: Params


class GetCommentPages(Schema):
    context: Post
    params: Params


class PagedResponse(ORMSchema):
    items: List[Any]
    page: int
    page_size: int
    pages: int
    total: int
