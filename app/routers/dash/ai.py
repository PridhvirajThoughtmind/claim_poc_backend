from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app import crud, schemas
from app.utills.openai_utils import get_openai_llm
from app.utills.prompts import QUERY_PROMPT

router = APIRouter()

async def _generate_ai_answer(query: str, patient_summary: str) -> str:
    llm_client = get_openai_llm()
    prompt = QUERY_PROMPT.format(patient_summary=patient_summary, query=query)

    response = llm_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
    )
    llm_response = response.choices[0].message.content
    return llm_response
@router.post("/generate-response", response_model=schemas.GenerateResponseResponse)
async def generate_response(request: schemas.GenerateResponseRequest, db: AsyncSession = Depends(get_db)):

    # fetch the clinical summary (uses app.crud.clinical_summaries.get_by_patient)
    clinical = await crud.clinical_summaries.get_by_patient(db=db,patient_id=int(request.patientId))
    summary_text = clinical.summary_text if clinical else ""

    # generate answer (replace with real AI call)
    answer = await _generate_ai_answer(query=request.query, patient_summary=summary_text)

    return schemas.GenerateResponseResponse(generatedResponse=answer)
