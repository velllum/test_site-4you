from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, validator, Field
from .base import (
    SuccessResponse,
    ListData
)


class Category(BaseModel):
    id: int 
    radio_id: int
    name: str
    color: str
    en: bool
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class CategorySuccessResponse(SuccessResponse):
    data: Category


class CategoryListData(ListData):
    items: List[Category] = []


class CategoryListSuccessResponse(SuccessResponse):
    data: CategoryListData


class NewCategory(BaseModel):
    name: str
    color: str
    