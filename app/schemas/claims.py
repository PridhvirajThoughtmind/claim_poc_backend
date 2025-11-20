from typing import List, Optional
from app.schemas.utils import StripStrBaseModel


# Shared properties
class ClaimBase(StripStrBaseModel):
    amount: float
    documents: Optional[List[str]] = None


# Properties to receive via API on creation
class ClaimCreateInput(StripStrBaseModel):
    amount: float
    documents: Optional[List[str]] = None


# Properties to receive in DB on creation
class ClaimCreate(ClaimBase):
    patient_id: int


# Properties to receive via API on update
class ClaimUpdateInput(StripStrBaseModel):
    amount: Optional[float] = None
    documents: Optional[List[str]] = None


# Properties to receive in DB on update
class ClaimUpdate(ClaimUpdateInput):
    patient_id: Optional[int] = None


class ClaimInDBBase(ClaimBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Claim(ClaimInDBBase):
    pass


# Additional properties stored in DB
class ClaimInDB(ClaimInDBBase):
    pass


# Property for pagination
class ClaimWithCount(StripStrBaseModel):
    total: int
    result: List[Claim]