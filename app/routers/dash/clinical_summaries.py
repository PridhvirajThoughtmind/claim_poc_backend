from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app import crud, schemas
import json

router = APIRouter()

@router.get("/{patient_id}/clinical-summary", response_model=schemas.ClinicalSummary)
async def read_clinical_summary(patient_id: int, db: AsyncSession = Depends(get_db)):
    clinical_summary = await crud.clinical_summaries.get_by_patient(db, patient_id)
    if not clinical_summary:
        raise HTTPException(status_code=404, detail="Clinical summary not found")
    return clinical_summary

@router.post("/{patient_id}/clinical-summary", response_model=schemas.ClinicalSummary, status_code=201)
async def create_clinical_summary(patient_id: int, clinical_summary: schemas.ClinicalSummaryCreateInput, db: AsyncSession = Depends(get_db)):
    # If summary_text is a JSON string, validate it
    summary_text = clinical_summary.summary_text
    if isinstance(summary_text, str):
        try:
            # Try to parse it as JSON to validate
            json.loads(summary_text)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="summary_text must be valid JSON or plain text")
    
    return await crud.clinical_summaries.create(
        db, 
        obj_in=schemas.ClinicalSummaryCreate(
            **clinical_summary.model_dump(), 
            patient_id=patient_id
        )
    )

@router.patch("/{patient_id}/clinical-summary", response_model=schemas.ClinicalSummary)
async def update_clinical_summary(patient_id: int, clinical_summary: schemas.ClinicalSummaryUpdateInput, db: AsyncSession = Depends(get_db)):
    db_clinical_summary = await crud.clinical_summaries.get_by_patient(db, patient_id)
    if not db_clinical_summary:
        raise HTTPException(status_code=404, detail="Clinical summary not found")
    
    # Validate summary_text if provided
    if clinical_summary.summary_text:
        try:
            json.loads(clinical_summary.summary_text)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="summary_text must be valid JSON or plain text")
    
    return await crud.clinical_summaries.update(
        db, 
        db_obj=db_clinical_summary, 
        obj_in=schemas.ClinicalSummaryUpdate(**clinical_summary.model_dump(), patient_id=patient_id)
    )

@router.delete("/{patient_id}/clinical-summary", status_code=204)
async def delete_clinical_summary(patient_id: int, db: AsyncSession = Depends(get_db)):
    db_clinical_summary = await crud.clinical_summaries.get_by_patient(db, patient_id)
    if not db_clinical_summary:
        raise HTTPException(status_code=404, detail="Clinical summary not found")
    await crud.clinical_summaries.remove(db, id=db_clinical_summary.id)