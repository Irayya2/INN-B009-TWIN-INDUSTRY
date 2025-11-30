"""
Inventory Routes
Handles spare parts inventory management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from pydantic import BaseModel

from database.connection import get_db
from models.spare_part import SparePart, PartStatus

router = APIRouter()

class InventoryResponse(BaseModel):
    id: int
    part_number: str
    name: str
    current_quantity: int
    min_quantity: int
    max_quantity: int
    status: str
    unit_cost: float
    total_value: float
    
    class Config:
        from_attributes = True

@router.get("/check")
async def check_inventory(
    low_stock_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    Check inventory status - implements SOP-SC-04: Spare Parts Inventory Check
    """
    query = select(SparePart)
    if low_stock_only:
        query = query.where(SparePart.current_quantity <= SparePart.min_quantity)
    
    result = await db.execute(query)
    parts = result.scalars().all()
    
    # Update status for each part
    for part in parts:
        if part.current_quantity <= 0:
            part.status = PartStatus.OUT_OF_STOCK
        elif part.current_quantity <= part.min_quantity:
            part.status = PartStatus.LOW_STOCK
        else:
            part.status = PartStatus.IN_STOCK
        
        part.total_value = part.current_quantity * part.unit_cost
    
    await db.commit()
    
    inventory_summary = {
        "total_parts": len(parts),
        "low_stock_count": sum(1 for p in parts if p.current_quantity <= p.min_quantity),
        "out_of_stock_count": sum(1 for p in parts if p.current_quantity == 0),
        "total_inventory_value": sum(p.total_value for p in parts),
        "parts": [InventoryResponse.model_validate(p) for p in parts]
    }
    
    return inventory_summary

@router.get("/{part_id}")
async def get_part_details(
    part_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific spare part"""
    result = await db.execute(
        select(SparePart).where(SparePart.id == part_id)
    )
    part = result.scalar_one_or_none()
    
    if not part:
        raise HTTPException(status_code=404, detail=f"Spare part {part_id} not found")
    
    return InventoryResponse.model_validate(part)











