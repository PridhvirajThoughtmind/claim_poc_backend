from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class Patients(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    progress = Column(String)
    quantity = Column(Integer)
    date = Column(Date)
    queries_count = Column(Integer, default=0)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))  # Add this line
    age = Column(Integer)  
    gender = Column(String)  
    phone = Column(String)  
    address = Column(Text)
    discharge_date = Column(Date)

    doctor_rel = relationship("Doctors", back_populates="patients_rel", uselist=False)
    insurance_rel = relationship("Insurance", back_populates="patients_rel", uselist=False)
    clinical_summary_rel = relationship("ClinicalSummaries", back_populates="patients_rel", uselist=False)
    queries_rel = relationship("Queries", back_populates="patients_rel")
    claims_rel = relationship("Claims", back_populates="patients_rel")
