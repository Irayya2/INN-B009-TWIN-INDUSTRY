"""
Alerts Routes
Handles alerts and warnings management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from database.connection import get_db
from models.alert import Alert, AlertStatus, AlertSeverity

router = APIRouter()

class AlertResponse(BaseModel):
    id: int
    machine_id: Optional[int]
    alert_type: str
    severity: str
    status: str
    title: str
    message: str
    fault_probability: Optional[float]
    predicted_failure_window: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/")
async def get_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all alerts with optional filtering
    """
    query = select(Alert).order_by(desc(Alert.created_at)).limit(limit)
    
    if status:
        try:
            status_enum = AlertStatus(status)
            query = query.where(Alert.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    if severity:
        try:
            severity_enum = AlertSeverity(severity)
            query = query.where(Alert.severity == severity_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid severity: {severity}")
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    
    return [AlertResponse.model_validate(a) for a in alerts]

@router.get("/active")
async def get_active_alerts(
    db: AsyncSession = Depends(get_db)
):
    """Get all active (unresolved) alerts"""
    result = await db.execute(
        select(Alert)
        .where(Alert.status == AlertStatus.ACTIVE)
        .order_by(desc(Alert.created_at))
    )
    alerts = result.scalars().all()
    
    return {
        "count": len(alerts),
        "alerts": [AlertResponse.model_validate(a) for a in alerts]
    }

@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: int,
    acknowledged_by: str,
    db: AsyncSession = Depends(get_db)
):
    """Acknowledge an alert"""
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id)
    )
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    
    alert.status = AlertStatus.ACKNOWLEDGED
    alert.acknowledged_by = acknowledged_by
    alert.acknowledged_at = datetime.utcnow()
    
    await db.commit()
    
    return {"message": "Alert acknowledged", "alert_id": alert_id}

@router.post("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Resolve an alert"""
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id)
    )
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    
    alert.status = AlertStatus.RESOLVED
    alert.resolved_at = datetime.utcnow()
    
    await db.commit()
    
    return {"message": "Alert resolved", "alert_id": alert_id}









