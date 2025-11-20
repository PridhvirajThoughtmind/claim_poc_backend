from typing import List, Optional
from app.schemas.utils import StripStrBaseModel


# Shared properties
class DoctorBase(StripStrBaseModel):
    name: str
    specialty: Optional[str] = None
    department: Optional[str] = None  
    diagnosis: Optional[str] = None  
    procedure: Optional[str] = None  


# Properties to receive via API on creation
class DoctorCreateInput(DoctorBase):
    pass


# Properties to receive in DB on creation
class DoctorCreate(DoctorBase):
    pass


# Properties to receive via API on update
class DoctorUpdateInput(StripStrBaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    department: Optional[str] = None  
    diagnosis: Optional[str] = None  
    procedure: Optional[str] = None  


# Properties to receive in DB on update
class DoctorUpdate(DoctorUpdateInput):
    pass


class DoctorInDBBase(DoctorBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Doctor(DoctorInDBBase):
    pass


# Additional properties stored in DB
class DoctorInDB(DoctorInDBBase):
    pass


# Property for pagination
class DoctorWithCount(StripStrBaseModel):
    total: int
    result: List[Doctor]