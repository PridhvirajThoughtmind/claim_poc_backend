from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.database import get_db
from app import crud, schemas

router = APIRouter()


@router.get("/", response_model=schemas.PatientWithCount)
async def read_patients(
    page: int = 1, limit: int = 10, search: str = None, status: str = None, db: AsyncSession = Depends(get_db)
):
    # The new get_multi returns a list of Patients with `doctor` attached per object.
    patients = await crud.patients.get_multi(db, search=search, status=status)
    total = len(patients)
    # apply pagination in the router for compatibility with existing response model
    offset = (page - 1) * limit
    result = patients[offset: offset + limit]
    return schemas.PatientWithCount(total=total, page=page, result=result)

@router.get("/{patient_id}", response_model=schemas.Patient)
async def read_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    patient = await crud.patients.get_detailed(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", response_model=schemas.Patient, status_code=201)
async def create_patient(patient: schemas.PatientCreateInput, db: AsyncSession = Depends(get_db)):
    db_patient = await crud.patients.create(db, obj_in=schemas.PatientCreate(**patient.model_dump()))
    await crud.patients.update_queries_count(db, patient_id=db_patient.id)
    return db_patient

@router.put("/{patient_id}", response_model=schemas.Patient)
async def update_patient(patient_id: int, patient: schemas.PatientUpdateInput, db: AsyncSession = Depends(get_db)):
    db_patient = await crud.patients.get(db, id=patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return await crud.patients.update(db, db_obj=db_patient, obj_in=schemas.PatientUpdate(**patient.model_dump()))

@router.delete("/{patient_id}", status_code=204)
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    db_patient = await crud.patients.get(db, id=patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    await crud.patients.remove(db, id=patient_id)
