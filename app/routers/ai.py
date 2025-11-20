from fastapi import APIRouter
from app.schemas.ai import GenerateResponseRequest, GenerateResponseResponse

router = APIRouter()

@router.post("/generate-response", response_model=GenerateResponseResponse)
async def generate_response(request: GenerateResponseRequest):
    # Mock AI response for POC
    return GenerateResponseResponse(generatedResponse=f"Mock response for query: {request.query} with context: {request.context}")
