from app.database.database import async_session
from app.models import Patients, Doctors, Insurance, Claims, Queries, ClinicalSummaries
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date

async def populate_db():
    async with async_session() as session:
        # Check if data already exists
        result = await session.execute(select(Patients).limit(1))
        if result.scalars().first():
            return  # Data already populated

        # Dummy data
        doctors = [
            Doctors(name="Dr. John Doe", specialty="Cardiology", department="Cardiology", diagnosis="Heart condition", procedure="Angioplasty"),  # Add new fields
            Doctors(name="Dr. Jane Smith", specialty="Neurology", department="Neurology", diagnosis="Brain injury", procedure="Surgery"),  # Add new fields
        ]
        session.add_all(doctors)
        await session.flush()

        patients = [
            Patients(name="Alice Johnson", progress="75%", quantity=5, date=date.today(), queries_count=0, doctor_id=doctors[0].id, age=45, gender="Female", phone="+91 9876543210", address="Bangalore, India", discharge_date=None),  # Add new fields
            Patients(name="Bob Wilson", progress="50%", quantity=3, date=date.today(), queries_count=0, doctor_id=doctors[1].id, age=50, gender="Male", phone="+91 9876543211", address="Mumbai, India", discharge_date=date.today()),  # Add new fields
        ]
        session.add_all(patients)
        await session.flush()

        insurance = [
            Insurance(patient_id=patients[0].id, provider="ABC Insurance", policy_number="POL123", coverage_type="Cashless", claim_requested=1000.0, claim_approved=800.0, status="Approved"),
            Insurance(patient_id=patients[1].id, provider="XYZ Insurance", policy_number="POL456", coverage_type="Reimbursement", claim_requested=500.0, claim_approved=400.0, status="Pending"),
        ]
        session.add_all(insurance)

        claims = [
            Claims(patient_id=patients[0].id, amount=800.0, documents=["doc1.pdf", "doc2.pdf"]),
        ]
        session.add_all(claims)

        queries = [
            Queries(patient_id=patients[0].id, question="What is the status of my claim?", raised_on=date.today(), answer="Your claim is approved."),
            Queries(patient_id=patients[1].id, question="How to file a claim?", raised_on=date.today(), answer="Please submit documents online."),
        ]
        session.add_all(queries)

        clinical_summaries = [
            ClinicalSummaries(patient_id=patients[0].id, summary_text="Patient has a history of heart issues."),
            ClinicalSummaries(patient_id=patients[1].id, summary_text="Patient is recovering from surgery."),
        ]
        session.add_all(clinical_summaries)

        await session.commit()