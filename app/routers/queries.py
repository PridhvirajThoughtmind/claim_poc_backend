from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.database import get_db
from app import crud, schemas
from datetime import date

router = APIRouter()

@router.get("/{patient_id}/queries", response_model=List[schemas.Query])
async def read_queries(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.queries.get_by_patient(db, patient_id)

@router.post("/{patient_id}/queries", response_model=schemas.Query, status_code=201)
async def create_query(patient_id: int, query: schemas.QueryCreateInput, db: AsyncSession = Depends(get_db)):
    db_query = await crud.queries.create(db, obj_in=schemas.QueryCreate(**query.model_dump(), patient_id=patient_id, raised_on=date.today()))
    await crud.patients.update_queries_count(db, patient_id=patient_id)
    return db_query

@router.patch("/{patient_id}/queries/{query_id}", response_model=schemas.Query)
async def update_query(patient_id: int, query_id: int, query: schemas.QueryUpdateInput, db: AsyncSession = Depends(get_db)):
    db_query = await crud.queries.get(db, id=query_id)
    if not db_query or db_query.patient_id != patient_id:
        raise HTTPException(status_code=404, detail="Query not found")
    return await crud.queries.update(db, db_obj=db_query, obj_in=schemas.QueryUpdate(**query.model_dump(), patient_id=patient_id))

@router.delete("/{patient_id}/queries/{query_id}", status_code=204)
async def delete_query(patient_id: int, query_id: int, db: AsyncSession = Depends(get_db)):
    db_query = await crud.queries.get(db, id=query_id)
    if not db_query or db_query.patient_id != patient_id:
        raise HTTPException(status_code=404, detail="Query not found")
    await crud.queries.remove(db, id=query_id)
    await crud.patients.update_queries_count(db, patient_id=patient_id)
