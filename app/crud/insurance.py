from app.crud.base import CRUDBase
from app.models.insurance import Insurance
from app.schemas.insurance import InsuranceCreate, InsuranceUpdate

class CrudInsurance(CRUDBase[Insurance, InsuranceCreate, InsuranceUpdate]):
    async def get_by_patient(self, db, patient_id: int):
        from sqlalchemy import select
        query = select(Insurance).where(Insurance.patient_id == patient_id)
        result = await db.execute(query)
        return result.scalars().first()

insurance = CrudInsurance(Insurance)
