from fastapi import FastAPI
from app.db_prestart import populate_db
from app.routers import patients,doctors, insurance, claims, queries, ai, dashboard

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await populate_db()


app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
app.include_router(insurance.router, prefix="/insurance", tags=["insurance"])
app.include_router(claims.router, prefix="/claims", tags=["claims"])
app.include_router(queries.router, prefix="/queries", tags=["queries"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "working"}
