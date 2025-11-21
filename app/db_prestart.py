from app.database.database import async_session, engine
from app.database.base_class import Base
from app.models import Patients, Doctors, Insurance, Claims, Queries, ClinicalSummaries
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from datetime import date
from pathlib import Path
import json

# Clinical summary descriptions for patients
ALICE_JOHNSON_DESCRIPTION = """## Clinical Summary - Alice Johnson

### Patient Overview
Alice Johnson is a 45-year-old female presenting with a comprehensive cardiac evaluation and management plan. Her medical history reveals a significant predisposition to cardiovascular complications, with multiple risk factors requiring careful monitoring and intervention. The patient has been under the care of Dr. John Doe from the Cardiology department, who has implemented a comprehensive treatment strategy to manage her condition.

### Medical History and Background
Alice has no known drug allergies and maintains a generally healthy lifestyle with occasional seasonal illnesses. Her past medical visits include a documented episode of sore throat and mild fever in November 2021, successfully treated with antibiotics, and a dermatological consultation in June 2023 for allergic dermatitis. These episodes were resolved without complications, indicating a favorable response to medical treatment.

### Current Clinical Assessment
The patient presents with stable cardiac function, though continuous monitoring is essential. Her progress has been rated at 75%, indicating substantial improvement in her overall health status. She has participated in five clinical encounters and has raised three queries regarding her treatment plan and claim status, demonstrating active engagement in her healthcare.

### Treatment Plan and Management
The cardiology team has implemented a comprehensive approach focusing on symptom management, risk reduction, and disease progression monitoring. Alice is compliant with her medication regimen and actively participates in follow-up appointments. The treatment plan emphasizes lifestyle modifications, including dietary changes, moderate exercise, and stress management techniques. Regular laboratory work and imaging studies are scheduled to assess cardiac function and detect any deterioration early.

### Insurance and Claims Status
Alice is covered under ABC Insurance with policy number POL123, which provides cashless treatment coverage. Her claim request of 1,000 has been approved for 800, reflecting the insurance company's assessment of covered expenses. The claim has been successfully processed and approved, providing financial support for her ongoing treatment and future medical interventions."""

BOB_WILSON_DESCRIPTION = """## Clinical Summary - Bob Wilson

### Patient Overview
Bob Wilson is a 50-year-old male with a significant cardiac history, currently admitted with acute exacerbation of coronary artery disease. He is under the comprehensive care of Dr. Jane Smith, a renowned neurologist from the Neurology department, who works collaboratively with the cardiology team to manage his complex medical condition. His presentation requires careful clinical coordination and multidisciplinary evaluation.

### Medical Background and Risk Factors
Bob has a documented history of hypertension, which has been a significant contributor to his current cardiac condition. He underwent an appendectomy in 2015, which was performed without complications. Additionally, he has a documented penicillin allergy that must be considered in all antibiotic selections. His past cardiology consultation in April 2022 identified stable angina, which has now progressed to require more intensive monitoring and intervention.

### Current Admission and Clinical Status
Bob was admitted on November 19, 2025, presenting with chest pain and breathlessness, triggering an urgent evaluation by the cardiology team. Upon admission, he was noted to be stable but dyspneic, classified as an Orange triage level indicating moderate urgency. His vital signs showed elevated blood pressure at 150/92 mmHg, tachycardia with a pulse of 98 beats per minute, and borderline oxygen saturation at 94% on room air.

### Diagnostic Findings and Laboratory Results
Comprehensive laboratory evaluation revealed borderline cardiac markers with troponin I at 0.04 ng/mL, suggesting possible myocardial injury. ECG findings demonstrated ST depression in leads V4-V6 with sinus tachycardia, consistent with acute coronary syndrome. Chest X-ray imaging revealed cardiomegaly, indicating cardiac enlargement. These findings collectively support the clinical suspicion of acute coronary syndrome requiring aggressive medical management and possible interventional procedures.

### Insurance and Financial Aspect
Bob's insurance coverage through XYZ Insurance with policy POL456 provides reimbursement-based coverage. His current claim request of 500 has been approved for 400, with the claim status currently pending final processing. The insurance company is reviewing additional documentation to finalize the reimbursement process. Expected discharge is planned for November 24, with cardiology follow-up scheduled for one week post-discharge."""

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
                Doctors(name="Dr. John Doe", specialty="Cardiology", department="Cardiology", diagnosis="Heart condition", procedure="Angioplasty"),
                Doctors(name="Dr. Jane Smith", specialty="Neurology", department="Neurology", diagnosis="Brain injury", procedure="Surgery"),
            ]
            session.add_all(doctors)
            await session.flush()

            patients = [
                Patients(name="Alice Johnson", progress="75%", quantity=5, date=date.today(), queries_count=0, doctor_id=doctors[0].id, age=45, gender="Female", phone="+91 9876543210", address="Bangalore, India", discharge_date=None),
                Patients(name="Bob Wilson", progress="50%", quantity=3, date=date.today(), queries_count=0, doctor_id=doctors[1].id, age=50, gender="Male", phone="+91 9876543211", address="Mumbai, India", discharge_date=date.today()),
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
                        
                        # Add descriptions based on patient index
                        description = ALICE_JOHNSON_DESCRIPTION if idx == 0 else BOB_WILSON_DESCRIPTION
                        
                        clinical_summaries.append(
                            ClinicalSummaries(patient_id=patient.id, summary_text=summary_text, description=description)
                        )
                except Exception:
                    # On parse error fall back to simple text summaries
                    clinical_summaries = [
                        ClinicalSummaries(patient_id=patients[0].id, summary_text="Patient has a history of heart issues.", description=ALICE_JOHNSON_DESCRIPTION),
                        ClinicalSummaries(patient_id=patients[1].id, summary_text="Patient is recovering from surgery.", description=BOB_WILSON_DESCRIPTION),
                    ]
            else:
                # If no dummy file, use simple text
                clinical_summaries = [
                    ClinicalSummaries(patient_id=patients[0].id, summary_text="Patient has a history of heart issues.", description=ALICE_JOHNSON_DESCRIPTION),
                    ClinicalSummaries(patient_id=patients[1].id, summary_text="Patient is recovering from surgery.", description=BOB_WILSON_DESCRIPTION),
                ]

            session.add_all(clinical_summaries)

            await session.commit()
    except Exception as e:
        print("Error populating database:", e)