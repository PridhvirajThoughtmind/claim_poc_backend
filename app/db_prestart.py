from app.database.database import async_session, engine
from app.database.base_class import Base
from app.models import Patients, Doctors, Insurance, Claims, Queries, ClinicalSummaries
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from datetime import date
from pathlib import Path
import json

async def populate_db():
    try:

        async with async_session() as session:
            # Check if data already exists
            try:
                result = await session.execute(select(Patients).limit(1))
            except ProgrammingError as e:
                # Tables probably don't exist yet (migration not applied) — create them and retry
                print("populate_db: database tables not present yet, creating tables:", e)
                # create tables from SQLAlchemy metadata using the async engine
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                # retry the select after creating tables
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
                Queries(patient_id=patients[0].id, question="What was the exact cause of admission?", raised_on=date.today()),
                Queries(patient_id=patients[0].id, question="What injuries were diagnosed upon admission?", raised_on=date.today()),
                Queries(patient_id=patients[0].id, question=" What procedures or imaging were done during admission?", raised_on=date.today()),
                Queries(patient_id=patients[1].id, question=" Is surgery planned or performed?", raised_on=date.today(), answer="Please submit documents online."),
            ]
            session.add_all(queries)

            # Load structured summaries from dummy.json (an array of patient summaries)
            project_root = Path(__file__).resolve().parent.parent
            print("project_root======", project_root)
            dummy_path = project_root / "dummy.json"
            clinical_summaries = []
            if dummy_path.exists():
                try:
                    with dummy_path.open("r", encoding="utf-8") as f:
                        data = json.load(f)

                    # If data is a dict (single patient), wrap it into a list
                    if isinstance(data, dict):
                        data = [data]

                    # Map each JSON entry to the seeded patients by index
                    for idx, patient in enumerate(patients):
                        if idx < len(data):
                            entry = data[idx]
                            summary_text = json.dumps(entry, ensure_ascii=False)
                        else:
                            # Fallback short text if no JSON provided for this patient
                            summary_text = json.dumps({"summary": "No structured summary available."})
                        clinical_summaries.append(
                            ClinicalSummaries(patient_id=patient.id, summary_text=summary_text)
                        )
                except Exception:
                    # On parse error fall back to simple text summaries
                    clinical_summaries = [
                        ClinicalSummaries(patient_id=patients[0].id, summary_text="Patient has a history of heart issues."),
                        ClinicalSummaries(patient_id=patients[1].id, summary_text="Patient is recovering from surgery."),
                    ]
            else:
                # If no dummy file, use simple text
                clinical_summaries = [
                    ClinicalSummaries(patient_id=patients[0].id, summary_text="Patient has a history of heart issues."),
                    ClinicalSummaries(patient_id=patients[1].id, summary_text="Patient is recovering from surgery."),
                ]

            session.add_all(clinical_summaries)

            await session.commit()
    except Exception as e:
        print("Error populating database:", e)