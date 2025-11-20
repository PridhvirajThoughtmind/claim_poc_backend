from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import List, Optional
from app.crud.base import CRUDBase
from app.models.patients import Patients
from app.schemas.patients import PatientCreate, PatientUpdate, PatientWithCount
from app.models.doctors import Doctors
from app.models.insurance import Insurance
from app.models.clinical_summaries import ClinicalSummaries
from app.models.queries import Queries
from sqlalchemy.orm import selectinload


class CrudPatient(CRUDBase[Patients, PatientCreate, PatientUpdate]):
    async def get_multi_with_pagination(
        self, db: AsyncSession, *, page: int = 1, limit: int = 10, search: Optional[str] = None, status: Optional[str] = None
    ) -> PatientWithCount:
        query = select(Patients)
        if search:
            query = query.where(Patients.name.ilike(f"%{search}%"))
        if status:
            query = query.join(Insurance).where(Insurance.status.ilike(f"%{status}%"))
        total = await db.scalar(select(func.count()).select_from(query.subquery()))
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        result = await db.execute(query)
        patients = result.scalars().all()
        return PatientWithCount(total=total, page=page, result=patients)

    async def get_detailed(self, db: AsyncSession, *, id: int) -> Optional[Patients]:
        query = select(Patients).options(
            selectinload(Patients.doctor_rel),  # Assuming relationships are defined in models
            selectinload(Patients.insurance_rel),
            selectinload(Patients.clinical_summary_rel),
            selectinload(Patients.queries_rel)
        ).where(Patients.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def update_queries_count(self, db: AsyncSession, *, patient_id: int):
        query_count = await db.scalar(select(func.count(Queries.id)).where(Queries.patient_id == patient_id))
        await db.execute(
            Patients.__table__.update().where(Patients.id == patient_id).values(queries_count=query_count)
        )
        await db.commit()

patients = CrudPatient(Patients)



