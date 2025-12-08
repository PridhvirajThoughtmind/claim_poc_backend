from pydantic import BaseModel
from typing import Optional


class ScribeRequest(BaseModel):
    """Request body for audio transcription"""
    pass  # Audio will be received as file upload, not in JSON body


class ScribeResponse(BaseModel):
    """Response body for transcription result"""
    doc_patient_conversation: str
    scribe: str
    status: str
    error: Optional[str] = None