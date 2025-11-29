"""
AI-Driven Industrial Twin for Predictive Maintenance and Supply Chain Continuity
Main FastAPI Application Entry Point
"""

# ===========================================================
# DISABLE ALL LOGGING (Uvicorn, SQLAlchemy, FastAPI, Alembic)
# ===========================================================
import logging

logging.disable(logging.CRITICAL)  # <-- turns OFF ALL logs globally
# ===========================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from database.connection import init_db, close_db
from routes import sensors, machines, faults, supply_chain, inventory, alerts, sop, maintenance


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n========== SERVER LINKS ==========")
    print("Frontend: http://localhost:5173")
    print("Backend:  http://localhost:8000")
    print("Docs:     http://localhost:8000/docs")
    print("API Base: http://localhost:8000")
    print("==================================\n")

    await init_db()
    yield
    await close_db()



app = FastAPI(
    title="Industrial Twin API",
    description="AI-Driven Predictive Maintenance and Supply Chain Continuity System",
    version="1.0.0",
    lifespan=lifespan
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ROUTERS
app.include_router(sensors.router, prefix="/api/sensors", tags=["Sensors"])
app.include_router(machines.router, prefix="/api/machines", tags=["Machines"])
app.include_router(faults.router, prefix="/api/faults", tags=["Faults"])
app.include_router(supply_chain.router, prefix="/api/supply", tags=["Supply Chain"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(sop.router, prefix="/api/sop", tags=["SOP"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["Maintenance"])


@app.get("/")
async def root():
    return {
        "message": "Industrial Twin API",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "industrial-twin-api"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="critical"  # <--- required to suppress uvicorn logs
    )
