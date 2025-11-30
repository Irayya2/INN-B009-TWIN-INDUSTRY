"""
Supply Chain Risk Routes
Handles supply chain continuity, risk assessment, and delay prediction
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from pydantic import BaseModel

from database.connection import get_db
from models.supply_chain_risk import SupplyChainRisk, RiskLevel
from models.spare_part import SparePart
from models.supplier import Supplier
from services.supply_chain_service import SupplyChainService

router = APIRouter()

class SupplyChainRiskResponse(BaseModel):
    spare_part_id: Optional[int]
    supplier_id: Optional[int]
    risk_level: str
    risk_score: float
    predicted_delay_days: Optional[float]
    stockout_probability: Optional[float]
    recommended_action: Optional[str]
    
    class Config:
        from_attributes = True

@router.get("/risk/{part_id}")
async def get_supply_chain_risk(
    part_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get supply chain risk assessment for a specific spare part
    Uses Prophet or regression models for delay prediction
    """
    # Get spare part
    result = await db.execute(
        select(SparePart).where(SparePart.id == part_id)
    )
    spare_part = result.scalar_one_or_none()
    
    if not spare_part:
        raise HTTPException(status_code=404, detail=f"Spare part {part_id} not found")
    
    # Initialize supply chain service
    supply_chain_service = SupplyChainService()
    
    # Get supplier if available
    supplier = None
    if spare_part.primary_supplier_id:
        result = await db.execute(
            select(Supplier).where(Supplier.id == spare_part.primary_supplier_id)
        )
        supplier = result.scalar_one_or_none()
    
    # Calculate risk assessment
    risk_assessment = await supply_chain_service.assess_risk(
        spare_part=spare_part,
        supplier=supplier,
        db=db
    )
    
    return risk_assessment

@router.get("/risk/all")
async def get_all_supply_chain_risks(
    db: AsyncSession = Depends(get_db)
):
    """Get supply chain risk assessment for all parts"""
    result = await db.execute(select(SparePart))
    spare_parts = result.scalars().all()
    
    risks = []
    supply_chain_service = SupplyChainService()
    
    for part in spare_parts:
        supplier = None
        if part.primary_supplier_id:
            result = await db.execute(
                select(Supplier).where(Supplier.id == part.primary_supplier_id)
            )
            supplier = result.scalar_one_or_none()
        
        risk_assessment = await supply_chain_service.assess_risk(
            spare_part=part,
            supplier=supplier,
            db=db
        )
        
        risks.append({
            "part_id": part.id,
            "part_number": part.part_number,
            "part_name": part.name,
            "current_quantity": part.current_quantity,
            "min_quantity": part.min_quantity,
            **risk_assessment
        })
    
    return {"risks": risks}

@router.get("/delay-prediction/{supplier_id}")
async def predict_delivery_delay(
    supplier_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Predict delivery delays for a supplier using time-series models
    """
    result = await db.execute(
        select(Supplier).where(Supplier.id == supplier_id)
    )
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise HTTPException(status_code=404, detail=f"Supplier {supplier_id} not found")
    
    supply_chain_service = SupplyChainService()
    
    delay_prediction = await supply_chain_service.predict_delivery_delay(
        supplier=supplier,
        db=db
    )
    
    return delay_prediction











