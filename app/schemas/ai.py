from pydantic import BaseModel


class GenerateResponseRequest(BaseModel):
    query: str
    patientId: str
    context: str


class GenerateResponseResponse(BaseModel):
    generatedResponse: str
