"""
Fault Prediction Routes
Handles ML-based fault prediction and anomaly detection
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from pydantic import BaseModel

from database.connection import get_db
from models.machine import Machine, MachineStatus
from models.sensor_data import SensorData
from services.fault_prediction import FaultPredictionService

router = APIRouter()

class FaultPredictionResponse(BaseModel):
    machine_id: str
    fault_probability: float
    anomaly_score: float
    predicted_failure_window: Optional[str]
    health_score: float
    status: str
    alert_level: str  # green, yellow, red
    risk_factors: list
    recommendations: list

@router.get("/predict/{machine_id}")
async def predict_fault(
    machine_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get ML-based fault prediction for a machine
    Uses LSTM/GRU, Isolation Forest, and Autoencoder models
    """
    # Get machine
    result = await db.execute(
        select(Machine).where(Machine.machine_id == machine_id)
    )
    machine = result.scalar_one_or_none()
    
    if not machine:
        raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")
    
    # Get recent sensor data (last 100 readings for ML model)
    result = await db.execute(
        select(SensorData)
        .where(SensorData.machine_id == machine.id)
        .order_by(desc(SensorData.timestamp))
        .limit(100)
    )
    sensor_readings = result.scalars().all()
    
    if len(sensor_readings) < 10:
        raise HTTPException(
            status_code=400,
            detail="Insufficient sensor data for prediction. Need at least 10 readings."
        )
    
    # Initialize prediction service
    prediction_service = FaultPredictionService()
    
    # Prepare data for ML models
    sensor_data_list = [
        {
            "vibration": sd.vibration,
            "temperature": sd.temperature,
            "acoustic_noise": sd.acoustic_noise,
            "load": sd.load,
            "rpm": sd.rpm
        }
        for sd in reversed(sensor_readings)  # Reverse to get chronological order
    ]
    
    # Run predictions
    prediction_result = await prediction_service.predict(
        machine_id=machine_id,
        sensor_data=sensor_data_list,
        machine=machine
    )
    
    # Update machine with latest predictions
    machine.fault_probability = prediction_result["fault_probability"]
    machine.anomaly_score = prediction_result["anomaly_score"]
    machine.health_score = prediction_result["health_score"]
    
    # Update status based on predictions
    if prediction_result["fault_probability"] > 70:
        machine.status = MachineStatus.CRITICAL
    elif prediction_result["fault_probability"] > 40:
        machine.status = MachineStatus.WARNING
    elif prediction_result["health_score"] < 60:
        machine.status = MachineStatus.WARNING
    else:
        machine.status = MachineStatus.OPERATIONAL
    
    await db.commit()
    
    return FaultPredictionResponse(
        machine_id=machine_id,
        fault_probability=prediction_result["fault_probability"],
        anomaly_score=prediction_result["anomaly_score"],
        predicted_failure_window=prediction_result.get("predicted_failure_window"),
        health_score=prediction_result["health_score"],
        status=machine.status.value,
        alert_level=prediction_result["alert_level"],
        risk_factors=prediction_result.get("risk_factors", []),
        recommendations=prediction_result.get("recommendations", [])
    )

@router.get("/predict/all")
async def predict_all_faults(
    db: AsyncSession = Depends(get_db)
):
    """Get fault predictions for all machines"""
    result = await db.execute(select(Machine))
    machines = result.scalars().all()
    
    predictions = []
    prediction_service = FaultPredictionService()
    
    for machine in machines:
        # Get recent sensor data
        result = await db.execute(
            select(SensorData)
            .where(SensorData.machine_id == machine.id)
            .order_by(desc(SensorData.timestamp))
            .limit(100)
        )
        sensor_readings = result.scalars().all()
        
        if len(sensor_readings) < 10:
            continue
        
        sensor_data_list = [
            {
                "vibration": sd.vibration,
                "temperature": sd.temperature,
                "acoustic_noise": sd.acoustic_noise,
                "load": sd.load,
                "rpm": sd.rpm
            }
            for sd in reversed(sensor_readings)
        ]
        
        prediction_result = await prediction_service.predict(
            machine_id=machine.machine_id,
            sensor_data=sensor_data_list,
            machine=machine
        )
        
        predictions.append({
            "machine_id": machine.machine_id,
            "name": machine.name,
            "fault_probability": prediction_result["fault_probability"],
            "anomaly_score": prediction_result["anomaly_score"],
            "health_score": prediction_result["health_score"],
            "alert_level": prediction_result["alert_level"]
        })
    
    return {"predictions": predictions}

