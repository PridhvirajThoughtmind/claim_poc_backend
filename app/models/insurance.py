from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class Insurance(Base):
    __tablename__ = "insurance"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    provider = Column(String)
    policy_number = Column(String)
    coverage_type = Column(String)
    claim_requested = Column(Float)
    claim_approved = Column(Float)
    status = Column(String)

    patients_rel = relationship("Patients", back_populates="insurance_rel")
