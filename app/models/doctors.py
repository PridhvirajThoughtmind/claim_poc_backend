from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class Doctors(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialty = Column(String)
    department = Column(String) 
    diagnosis = Column(String) 
    procedure = Column(String)

    patients_rel = relationship("Patients", back_populates="doctor_rel")
