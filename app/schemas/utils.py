from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class DatabaseAction(Enum):
    COMMIT = "COMMIT"
    FLUSH = "FLUSH"
    

class StripStrBaseModel(BaseModel):
    """Base model that strips whitespace from string fields"""
    
    @field_validator("*", mode="before")
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v