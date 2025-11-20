from pydantic import BaseModel


class GenerateResponseRequest(BaseModel):
    query: str
    patientId: str


class GenerateResponseResponse(BaseModel):
    generatedResponse: str
