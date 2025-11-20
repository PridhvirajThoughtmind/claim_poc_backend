from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/{patient_id}/insurance", response_model=schemas.Insurance)
async def read_insurance(patient_id: int, db: AsyncSession = Depends(get_db)):
    insurance = await crud.insurance.get_by_patient(db, patient_id)
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return insurance

@router.put("/{patient_id}/insurance", response_model=schemas.Insurance)
async def update_insurance(patient_id: int, insurance: schemas.InsuranceUpdateInput, db: AsyncSession = Depends(get_db)):
    db_insurance = await crud.insurance.get_by_patient(db, patient_id)
    if not db_insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return await crud.insurance.update(db, db_obj=db_insurance, obj_in=schemas.InsuranceUpdate(**insurance.model_dump(), patient_id=patient_id))
