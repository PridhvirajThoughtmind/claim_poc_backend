from datetime import date
from typing import List, Optional
from app.schemas.utils import StripStrBaseModel


# Shared properties
class QueryBase(StripStrBaseModel):
    question: str
    raised_on: Optional[date] = None
    answer: Optional[str] = None


# Properties to receive via API on creation
class QueryCreateInput(StripStrBaseModel):
    question: str


# Properties to receive in DB on creation
class QueryCreate(QueryBase):
    patient_id: int
    raised_on: date


# Properties to receive via API on update
class QueryUpdateInput(StripStrBaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None


# Properties to receive in DB on update
class QueryUpdate(QueryUpdateInput):
    patient_id: Optional[int] = None
    raised_on: Optional[date] = None


class QueryInDBBase(QueryBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Query(QueryInDBBase):
    pass


# Additional properties stored in DB
class QueryInDB(QueryInDBBase):
    pass


# Property for pagination
class QueryWithCount(StripStrBaseModel):
    total: int
    result: List[Query]
