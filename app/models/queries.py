from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class Queries(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    question = Column(String)
    raised_on = Column(Date)
    answer = Column(String)

    patients_rel = relationship("Patients", back_populates="queries_rel")
