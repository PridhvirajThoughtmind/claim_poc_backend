from sqlalchemy import Column, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class ClinicalSummaries(Base):
    __tablename__ = "clinical_summaries"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    summary_text = Column(Text)
    description = Column(Text)

    patients_rel = relationship("Patients", back_populates="clinical_summary_rel")
