from app.crud.base import CRUDBase
from app.models.clinical_summaries import ClinicalSummaries
from app.schemas.clinical_summary import ClinicalSummaryCreate, ClinicalSummaryUpdate

class CrudClinicalSummary(CRUDBase[ClinicalSummaries, ClinicalSummaryCreate, ClinicalSummaryUpdate]):
    async def get_by_patient(self, db, patient_id: int):
        from sqlalchemy import select
        query = select(ClinicalSummaries).where(ClinicalSummaries.patient_id == patient_id)
        result = await db.execute(query)
        return result.scalars().first()

clinical_summaries = CrudClinicalSummary(ClinicalSummaries)
