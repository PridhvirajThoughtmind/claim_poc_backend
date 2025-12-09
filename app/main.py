from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db_prestart import populate_db
from app.routers.dash import patients, doctors, insurance, claims, queries, ai, dashboard, clinical_summaries

from app.routers.scribe import scribe

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Populating DB with initial data if necessary...")
    await populate_db()

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "working"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
app.include_router(insurance.router, prefix="/insurance", tags=["insurance"])
app.include_router(claims.router, prefix="/claims", tags=["claims"])
app.include_router(queries.router, prefix="/queries", tags=["queries"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(clinical_summaries.router, prefix="/clinical-summaries", tags=["clinical_summaries"])
app.include_router(scribe.router, prefix="/scribe", tags=["scribe"])

