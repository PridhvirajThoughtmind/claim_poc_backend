from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app import crud, schemas

router = APIRouter()

@router.post("/{patient_id}/claims", response_model=schemas.Claim, status_code=201)
async def create_claim(patient_id: int, claim: schemas.ClaimCreateInput, db: AsyncSession = Depends(get_db)):
    return await crud.claims.create(db, obj_in=schemas.ClaimCreate(**claim.model_dump(), patient_id=patient_id))
