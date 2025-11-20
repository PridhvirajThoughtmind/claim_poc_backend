# Import all the models.
# So that Base has them before being imported by Alembic.
from app.database.base_class import Base
from app.models.patients import Patients
from app.models.claims import Claims
from app.models.clinical_summaries import ClinicalSummaries
from app.models.insurance import Insurance
from app.models.doctors import Doctors
from app.models.queries import Queries