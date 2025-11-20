from app.crud.base import CRUDBase
from app.models.doctors import Doctors
from app.schemas.doctors import DoctorCreate, DoctorUpdate

class CrudDoctor(CRUDBase[Doctors, DoctorCreate, DoctorUpdate]):
    pass

doctors = CrudDoctor(Doctors)
