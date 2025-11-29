"""
Machine Routes
Handles machine information, status, and health metrics
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from database.connection import get_db
from models.machine import Machine, MachineStatus
from models.sensor_data import SensorData

router = APIRouter()

class MachineResponse(BaseModel):
    id: int
    machine_id: str
    name: str
    machine_type: str
    status: str
    health_score: float
    fault_probability: float
    anomaly_score: float
    location: Optional[str]
    department: Optional[str]
    last_maintenance_date: Optional[datetime]
    next_maintenance_date: Optional[datetime]
    downtime_cost_per_hour: float
    
    class Config:
        from_attributes = True

class MachineCreate(BaseModel):
    machine_id: str
    name: str
    machine_type: str
    max_rpm: Optional[float] = None
    max_temperature: Optional[float] = None
    max_vibration: Optional[float] = None
    max_load: Optional[float] = None
    location: Optional[str] = None
    department: Optional[str] = None
    downtime_cost_per_hour: float = 1000.0

@router.get("/")
async def get_all_machines(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all machines with optional status filter"""
    query = select(Machine)
    if status:
        try:
            status_enum = MachineStatus(status)
            query = query.where(Machine.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    result = await db.execute(query)
    machines = result.scalars().all()
    
    return [MachineResponse.model_validate(m) for m in machines]

@router.get("/{machine_id}")
async def get_machine_status(
    machine_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed machine status and health metrics"""
    result = await db.execute(
        select(Machine).where(Machine.machine_id == machine_id)
    )
    machine = result.scalar_one_or_none()
    
    if not machine:
        raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")
    
    # Get latest sensor reading
    result = await db.execute(
        select(SensorData)
        .where(SensorData.machine_id == machine.id)
        .order_by(desc(SensorData.timestamp))
        .limit(1)
    )
    latest_sensor = result.scalar_one_or_none()
    
    response = MachineResponse.model_validate(machine)
    response_dict = response.model_dump()
    
    if latest_sensor:
        response_dict["latest_sensor_data"] = {
            "vibration": latest_sensor.vibration,
            "temperature": latest_sensor.temperature,
            "acoustic_noise": latest_sensor.acoustic_noise,
            "load": latest_sensor.load,
            "rpm": latest_sensor.rpm,
            "timestamp": latest_sensor.timestamp
        }
    
    return response_dict

@router.post("/")
async def create_machine(
    machine: MachineCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new machine"""
    # Check if machine_id already exists
    result = await db.execute(
        select(Machine).where(Machine.machine_id == machine.machine_id)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail=f"Machine {machine.machine_id} already exists")
    
    new_machine = Machine(
        machine_id=machine.machine_id,
        name=machine.name,
        machine_type=machine.machine_type,
        max_rpm=machine.max_rpm,
        max_temperature=machine.max_temperature,
        max_vibration=machine.max_vibration,
        max_load=machine.max_load,
        location=machine.location,
        department=machine.department,
        downtime_cost_per_hour=machine.downtime_cost_per_hour,
        status=MachineStatus.OPERATIONAL
    )
    
    db.add(new_machine)
    await db.commit()
    await db.refresh(new_machine)
    
    return MachineResponse.model_validate(new_machine)

@router.get("/status/all")
async def get_all_machines_status(
    db: AsyncSession = Depends(get_db)
):
    """Get health status overview for all machines"""
    result = await db.execute(select(Machine))
    machines = result.scalars().all()
    
    status_summary = {
        "total_machines": len(machines),
        "operational": 0,
        "warning": 0,
        "critical": 0,
        "maintenance": 0,
        "offline": 0,
        "average_health_score": 0.0,
        "machines": []
    }
    
    total_health = 0.0
    for machine in machines:
        status_key = machine.status.value
        status_summary[status_key] = status_summary.get(status_key, 0) + 1
        total_health += machine.health_score
        status_summary["machines"].append({
            "machine_id": machine.machine_id,
            "name": machine.name,
            "status": machine.status.value,
            "health_score": machine.health_score,
            "fault_probability": machine.fault_probability
        })
    
    if machines:
        status_summary["average_health_score"] = total_health / len(machines)
    
    return status_summary

