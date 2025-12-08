from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.database import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/", response_model=schemas.DoctorWithCount)
async def read_doctors(
    page: int = 1, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    # Assuming CrudDoctor has a get_multi_with_pagination method similar to patients
    # If not, implement it or use fetch_all for simplicity
    doctors = await crud.doctors.fetch_all(db)
    total = len(doctors)
    offset = (page - 1) * limit
    result = doctors[offset:offset + limit]
    return schemas.DoctorWithCount(total=total, result=result)

@router.get("/{doctor_id}", response_model=schemas.Doctor)
async def read_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    doctor = await crud.doctors.get(db, id=doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/", response_model=schemas.Doctor, status_code=201)
async def create_doctor(doctor: schemas.DoctorCreateInput, db: AsyncSession = Depends(get_db)):
    return await crud.doctors.create(db, obj_in=schemas.DoctorCreate(**doctor.model_dump()))

@router.patch("/{doctor_id}", response_model=schemas.Doctor)
async def update_doctor(doctor_id: int, doctor: schemas.DoctorUpdateInput, db: AsyncSession = Depends(get_db)):
    db_doctor = await crud.doctors.get(db, id=doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return await crud.doctors.update(db, db_obj=db_doctor, obj_in=schemas.DoctorUpdate(**doctor.model_dump()))

@router.delete("/{doctor_id}", status_code=204)
async def delete_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    db_doctor = await crud.doctors.get(db, id=doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    await crud.doctors.remove(db, id=doctor_id)