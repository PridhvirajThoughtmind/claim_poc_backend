from sqlalchemy import Column, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class Claims(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    amount = Column(Float)
    documents = Column(JSON)

    patients_rel = relationship("Patients", back_populates="claims_rel")
