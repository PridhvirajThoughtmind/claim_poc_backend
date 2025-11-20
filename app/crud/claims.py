from app.crud.base import CRUDBase
from app.models.claims import Claims
from app.schemas.claims import ClaimCreate, ClaimUpdate

class CrudClaim(CRUDBase[Claims, ClaimCreate, ClaimUpdate]):
    pass

claims = CrudClaim(Claims)
