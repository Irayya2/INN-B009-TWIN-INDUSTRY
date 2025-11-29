"""
Sensor Data Routes
Handles real-time sensor data ingestion and retrieval
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from database.connection import get_db
from models.sensor_data import SensorData
from models.machine import Machine

router = APIRouter()

class SensorReading(BaseModel):
    machine_id: str
    vibration: float
    temperature: float
    acoustic_noise: float
    load: float
    rpm: float

class SensorReadingResponse(BaseModel):
    id: int
    machine_id: int
    vibration: float
    temperature: float
    acoustic_noise: float
    load: float
    rpm: float
    timestamp: datetime
    is_anomaly: int
    anomaly_score: float
    
    class Config:
        from_attributes = True

@router.post("/push")
async def push_sensor_data(
    reading: SensorReading,
    db: AsyncSession = Depends(get_db)
):
    """
    Store live sensor data from machines
    This endpoint receives real-time sensor readings and stores them in the database
    """
    # Find machine by machine_id (string identifier)
    result = await db.execute(
        select(Machine).where(Machine.machine_id == reading.machine_id)
    )
    machine = result.scalar_one_or_none()
    
    if not machine:
        raise HTTPException(status_code=404, detail=f"Machine {reading.machine_id} not found")
    
    # Create sensor data entry
    sensor_data = SensorData(
        machine_id=machine.id,
        vibration=reading.vibration,
        temperature=reading.temperature,
        acoustic_noise=reading.acoustic_noise,
        load=reading.load,
        rpm=reading.rpm
    )
    
    db.add(sensor_data)
    await db.commit()
    await db.refresh(sensor_data)
    
    # Trigger anomaly detection (async background task would be better in production)
    # For now, we'll call it synchronously
    
    return {
        "message": "Sensor data stored successfully",
        "sensor_id": sensor_data.id,
        "timestamp": sensor_data.timestamp
    }

@router.get("/latest/{machine_id}")
async def get_latest_sensor_data(
    machine_id: str,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get latest sensor readings for a machine"""
    result = await db.execute(
        select(Machine).where(Machine.machine_id == machine_id)
    )
    machine = result.scalar_one_or_none()
    
    if not machine:
        raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")
    
    result = await db.execute(
        select(SensorData)
        .where(SensorData.machine_id == machine.id)
        .order_by(desc(SensorData.timestamp))
        .limit(limit)
    )
    sensor_data = result.scalars().all()
    
    return [SensorReadingResponse.model_validate(sd) for sd in sensor_data]

@router.get("/timeframe/{machine_id}")
async def get_sensor_data_timeframe(
    machine_id: str,
    hours: int = 24,
    db: AsyncSession = Depends(get_db)
):
    """Get sensor data for a specific time window"""
    result = await db.execute(
        select(Machine).where(Machine.machine_id == machine_id)
    )
    machine = result.scalar_one_or_none()
    
    if not machine:
        raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")
    
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    result = await db.execute(
        select(SensorData)
        .where(
            SensorData.machine_id == machine.id,
            SensorData.timestamp >= start_time
        )
        .order_by(SensorData.timestamp)
    )
    sensor_data = result.scalars().all()
    
    return [SensorReadingResponse.model_validate(sd) for sd in sensor_data]









