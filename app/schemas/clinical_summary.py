from typing import List, Optional, Dict, Any, Union
from pydantic import Field, field_validator
import json
from app.schemas.utils import StripStrBaseModel


# Shared properties
class ClinicalSummaryBase(StripStrBaseModel):
    summary_text: str = Field(..., description="Medical summary as JSON string or plain text")
    description: Optional[str] = Field(None, description="Detailed description in markdown format")
    
    @field_validator("summary_text", mode="before")
    @classmethod
    def validate_summary_text(cls, v):
        """Accept both JSON string and plain text, convert dict to JSON string"""
        if v is None:
            raise ValueError("summary_text is required")
        
        # If it's a dict, convert to JSON string
        if isinstance(v, dict):
            return json.dumps(v, ensure_ascii=False)
        
        # If it's a string, validate if it's JSON or plain text
        if isinstance(v, str):
            try:
                # Try to parse as JSON to validate
                json.loads(v)
                return v
            except json.JSONDecodeError:
                # It's plain text, which is also acceptable
                return v
        
        raise ValueError("summary_text must be a string (JSON or plain text) or dict")


# Properties to receive via API on creation
class ClinicalSummaryCreateInput(StripStrBaseModel):
    summary_text: str = Field(..., description="Medical summary as JSON string or plain text")
    description: Optional[str] = Field(None, description="Detailed description in markdown format")
    
    @field_validator("summary_text", mode="before")
    @classmethod
    def validate_summary_text(cls, v):
        """Accept both JSON string and plain text, convert dict to JSON string"""
        if v is None:
            raise ValueError("summary_text is required")
        
        if isinstance(v, dict):
            return json.dumps(v, ensure_ascii=False)
        
        if isinstance(v, str):
            try:
                json.loads(v)
                return v
            except json.JSONDecodeError:
                return v
        
        raise ValueError("summary_text must be a string (JSON or plain text) or dict")


# Properties to receive in DB on creation
class ClinicalSummaryCreate(ClinicalSummaryBase):
    patient_id: int = Field(..., description="Patient ID")


# Properties to receive via API on update
class ClinicalSummaryUpdateInput(StripStrBaseModel):
    summary_text: Optional[str] = Field(None, description="Medical summary as JSON string or plain text")
    description: Optional[str] = Field(None, description="Detailed description in markdown format")
    
    @field_validator("summary_text", mode="before")
    @classmethod
    def validate_summary_text(cls, v):
        """Accept both JSON string and plain text, convert dict to JSON string"""
        if v is None:
            return v
        
        if isinstance(v, dict):
            return json.dumps(v, ensure_ascii=False)
        
        if isinstance(v, str):
            try:
                json.loads(v)
                return v
            except json.JSONDecodeError:
                return v
        
        raise ValueError("summary_text must be a string (JSON or plain text) or dict")


# Properties to receive in DB on update
class ClinicalSummaryUpdate(ClinicalSummaryUpdateInput):
    patient_id: Optional[int] = Field(None, description="Patient ID")


class ClinicalSummaryInDBBase(ClinicalSummaryBase):
    id: int = Field(..., description="Clinical summary ID")
    patient_id: int = Field(..., description="Patient ID")

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
    total: int = Field(..., description="Total count of clinical summaries")
    result: List[ClinicalSummary] = Field(..., description="List of clinical summaries")