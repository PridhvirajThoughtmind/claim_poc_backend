from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import List, Optional
from app.crud.base import CRUDBase
from app import crud
from app.models.patients import Patients
from app.schemas.patients import PatientCreate, PatientUpdate, PatientWithCount
from app.models.doctors import Doctors
from app.models.insurance import Insurance
from app.models.clinical_summaries import ClinicalSummaries
from app.models.queries import Queries
from sqlalchemy.orm import selectinload


class CrudPatient(CRUDBase[Patients, PatientCreate, PatientUpdate]):
    async def get_multi(self, db: AsyncSession, *, search: Optional[str] = None, status: Optional[str] = None):
        """Fetch all patients (optionally filtered) and attach doctor and insurance summary."""
        # eager-load related doctor and insurance to avoid N+1
        query = select(Patients).options(selectinload(Patients.doctor_rel), selectinload(Patients.insurance_rel))
        if search:
            query = query.where(Patients.name.ilike(f"%{search}%"))
        if status:
            query = query.join(Insurance).where(Insurance.status.ilike(f"%{status}%"))

        result = await db.execute(query)
        patients = result.scalars().all()
        for p in patients:
                # doctor: prefer loaded relation, fallback to CRUD get()

                # insurance (we only attach provider and status for the list view)
                try:
                    if getattr(p, "doctor_rel", None):
                        setattr(p, "doctor", p.doctor_rel)
                    # prefer loaded relation
                    if getattr(p, "insurance_rel", None):
                        ins = p.insurance_rel
                        setattr(p, "insurance_provider", getattr(ins, "provider", None))
                        setattr(p, "claim_status", getattr(ins, "status", None))
                except Exception:
                     setattr(p, "insurance_provider", None)
                     setattr(p, "claim_status", None)

        return patients

    async def get_detailed(self, db: AsyncSession, *, id: int) -> Optional[Patients]:
        query = select(Patients).options(
            selectinload(Patients.doctor_rel),  # Assuming relationships are defined in models
            selectinload(Patients.insurance_rel),
            selectinload(Patients.clinical_summary_rel),
            selectinload(Patients.queries_rel)
        ).where(Patients.id == id)
        result = await db.execute(query)
        patient = result.scalars().first()
        if getattr(patient, "doctor_rel", None):
            setattr(patient, "doctor", patient.doctor_rel)
        if getattr(patient, "insurance_rel", None):
            ins = patient.insurance_rel
            setattr(patient, "insurance_provider", getattr(ins, "provider", None))
            setattr(patient, "claim_status", getattr(ins, "status", None))

        return patient
    
    async def update_queries_count(self, db: AsyncSession, *, patient_id: int):
        query_count = await db.scalar(select(func.count(Queries.id)).where(Queries.patient_id == patient_id))
        await db.execute(
            Patients.__table__.update().where(Patients.id == patient_id).values(queries_count=query_count)
        )
        await db.commit()

patients = CrudPatient(Patients)



