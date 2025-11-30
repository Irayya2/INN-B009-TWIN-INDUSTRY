"""
Maintenance Routes
Handles maintenance scheduling and logs
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from database.connection import get_db
from models.maintenance_log import MaintenanceLog, MaintenanceType, MaintenanceStatus
from models.machine import Machine

router = APIRouter()

class MaintenanceLogResponse(BaseModel):
    id: int
    machine_id: int
    maintenance_type: str
    status: str
    title: str
    scheduled_date: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    cost: Optional[float]
    sop_reference: Optional[str]
    
    class Config:
        from_attributes = True

class MaintenanceScheduleRequest(BaseModel):
    machine_id: str
    maintenance_type: str
    title: str
    description: Optional[str]
    scheduled_date: datetime
    technician: Optional[str] = None
    sop_reference: Optional[str] = None

@router.post("/schedule")
async def schedule_maintenance(
    request: MaintenanceScheduleRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Schedule a maintenance activity - implements SOP-MAINT-02: Predictive Maintenance Scheduling
    """
    # Find machine
    result = await db.execute(
        select(Machine).where(Machine.machine_id == request.machine_id)
    )
    machine = result.scalar_one_or_none()
    
    if not machine:
        raise HTTPException(status_code=404, detail=f"Machine {request.machine_id} not found")
    
    try:
        maintenance_type_enum = MaintenanceType(request.maintenance_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid maintenance type: {request.maintenance_type}")
    
    new_maintenance = MaintenanceLog(
        machine_id=machine.id,
        maintenance_type=maintenance_type_enum,
        title=request.title,
        description=request.description,
        scheduled_date=request.scheduled_date,
        technician=request.technician,
        sop_reference=request.sop_reference,
        status=MaintenanceStatus.SCHEDULED
    )
    
    # Update machine's next maintenance date
    machine.next_maintenance_date = request.scheduled_date
    
    db.add(new_maintenance)
    await db.commit()
    await db.refresh(new_maintenance)
    
    return MaintenanceLogResponse.model_validate(new_maintenance)

@router.get("/logs")
async def get_maintenance_logs(
    machine_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get maintenance logs with optional filtering"""
    query = select(MaintenanceLog).order_by(desc(MaintenanceLog.scheduled_date)).limit(limit)
    
    if machine_id:
        result = await db.execute(
            select(Machine).where(Machine.machine_id == machine_id)
        )
        machine = result.scalar_one_or_none()
        if machine:
            query = query.where(MaintenanceLog.machine_id == machine.id)
        else:
            raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")
    
    if status:
        try:
            status_enum = MaintenanceStatus(status)
            query = query.where(MaintenanceLog.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    result = await db.execute(query)
    logs = result.scalars().all()
    
    return [MaintenanceLogResponse.model_validate(log) for log in logs]











