from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.database import async_session
from app.database.database import get_db
from app.models.patients import Patients
from app.models.insurance import Insurance

router = APIRouter()

@router.get("/patients/summary")
async def get_patients_summary(db: AsyncSession = Depends(get_db)):
    total_patients = await db.scalar(select(func.count(Patients.id)))
    pending_claims = await db.scalar(select(func.count(Insurance.id)).where(Insurance.status == "Pending"))
    approved_claims = await db.scalar(select(func.count(Insurance.id)).where(Insurance.status == "Approved"))
    return {"totalPatients": total_patients, "pendingClaims": pending_claims, "approvedClaims": approved_claims}
