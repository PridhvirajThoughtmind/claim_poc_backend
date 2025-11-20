from app.crud.base import CRUDBase
from app.models.queries import Queries
from app.schemas.queries import QueryCreate, QueryUpdate
from sqlalchemy import select

class CrudQuery(CRUDBase[Queries, QueryCreate, QueryUpdate]):
    async def get_by_patient(self, db, patient_id: int):
        query = select(Queries).where(Queries.patient_id == patient_id)
        result = await db.execute(query)
        return result.scalars().all()

queries = CrudQuery(Queries)
