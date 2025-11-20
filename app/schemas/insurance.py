from typing import List, Optional
from app.schemas.utils import StripStrBaseModel


# Shared properties
class InsuranceBase(StripStrBaseModel):
    provider: str
    policy_number: str
    coverage_type: Optional[str] = None
    claim_requested: Optional[float] = None
    claim_approved: Optional[float] = None
    status: Optional[str] = None


# Properties to receive via API on creation
class InsuranceCreateInput(StripStrBaseModel):
    provider: str
    policy_number: str
    coverage_type: Optional[str] = None
    claim_requested: Optional[float] = None
    claim_approved: Optional[float] = None
    status: Optional[str] = None


# Properties to receive in DB on creation
class InsuranceCreate(InsuranceBase):
    patient_id: int


# Properties to receive via API on update
class InsuranceUpdateInput(StripStrBaseModel):
    provider: Optional[str] = None
    policy_number: Optional[str] = None
    coverage_type: Optional[str] = None
    claim_requested: Optional[float] = None
    claim_approved: Optional[float] = None
    status: Optional[str] = None


# Properties to receive in DB on update
class InsuranceUpdate(InsuranceUpdateInput):
    patient_id: Optional[int] = None


class InsuranceInDBBase(InsuranceBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Insurance(InsuranceInDBBase):
    pass


# Additional properties stored in DB
class InsuranceInDB(InsuranceInDBBase):
    pass


# Property for pagination
class InsuranceWithCount(StripStrBaseModel):
    total: int
    result: List[Insurance]