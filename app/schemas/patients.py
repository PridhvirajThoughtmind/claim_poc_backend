from datetime import datetime
from typing import List, Optional
from app.schemas.utils import StripStrBaseModel
from app.schemas.doctors import Doctor


# Shared properties
class PatientBase(StripStrBaseModel):
    name: str
    progress: Optional[str] = None
    quantity: Optional[int] = None
    date: Optional[datetime] = None
    age: Optional[int] = None 
    gender: Optional[str] = None 
    phone: Optional[str] = None 
    address: Optional[str] = None 
    discharge_date: Optional[datetime] = None


# Properties to receive via API on creation
class PatientCreateInput(PatientBase):
    pass


# Properties to receive in DB on creation
class PatientCreate(PatientBase):
    queries_count: int = 0


# Properties to receive via API on update
class PatientUpdateInput(StripStrBaseModel):
    name: Optional[str] = None
    progress: Optional[str] = None
    quantity: Optional[int] = None
    date: Optional[datetime] = None
    age: Optional[int] = None  # New field
    gender: Optional[str] = None  # New field
    phone: Optional[str] = None  # New field
    address: Optional[str] = None  # New field
    discharge_date: Optional[datetime] = None  # New field


# Properties to receive in DB on update
class PatientUpdate(PatientUpdateInput):
    queries_count: Optional[int] = None


class PatientInDBBase(PatientBase):
    id: int
    queries_count: int
    doctor: Optional[Doctor] = None
    insurance_provider: Optional[str] = None
    claim_status: Optional[str] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Patient(PatientInDBBase):
    pass


# Additional properties stored in DB
class PatientInDB(PatientInDBBase):
    pass


# Property for pagination
class PatientWithCount(StripStrBaseModel):
    total: int
    page: int
    result: List[Patient]