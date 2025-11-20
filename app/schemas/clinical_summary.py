from typing import List, Optional
from app.schemas.utils import StripStrBaseModel


# Shared properties
class ClinicalSummaryBase(StripStrBaseModel):
    summary_text: str


# Properties to receive via API on creation
class ClinicalSummaryCreateInput(StripStrBaseModel):
    summary_text: str


# Properties to receive in DB on creation
class ClinicalSummaryCreate(ClinicalSummaryBase):
    patient_id: int


# Properties to receive via API on update
class ClinicalSummaryUpdateInput(StripStrBaseModel):
    summary_text: Optional[str] = None


# Properties to receive in DB on update
class ClinicalSummaryUpdate(ClinicalSummaryUpdateInput):
    patient_id: Optional[int] = None


class ClinicalSummaryInDBBase(ClinicalSummaryBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class ClinicalSummary(ClinicalSummaryInDBBase):
    pass


# Additional properties stored in DB
class ClinicalSummaryInDB(ClinicalSummaryInDBBase):
    pass


# Property for pagination
class ClinicalSummaryWithCount(StripStrBaseModel):
    total: int
    result: List[ClinicalSummary]