"""
SOP (Standard Operating Procedure) Routes
Handles SOP workflow management and task tracking
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from database.connection import get_db
from models.sop_task import SOPTask, SOPTaskStatus, SOPCode
from models.machine import Machine

router = APIRouter()

class SOPTaskResponse(BaseModel):
    id: int
    machine_id: Optional[int]
    sop_code: str
    task_name: str
    description: Optional[str]
    status: str
    priority: str
    scheduled_date: datetime
    due_date: Optional[datetime]
    assigned_to: Optional[str]
    
    class Config:
        from_attributes = True

class SOPTaskCreate(BaseModel):
    machine_id: Optional[str] = None
    sop_code: str
    task_name: str
    description: Optional[str] = None
    scheduled_date: datetime
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    priority: str = "medium"

@router.get("/tasks")
async def get_sop_tasks(
    status: Optional[str] = None,
    sop_code: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all SOP tasks with optional filtering
    """
    query = select(SOPTask).order_by(desc(SOPTask.scheduled_date))
    
    if status:
        try:
            status_enum = SOPTaskStatus(status)
            query = query.where(SOPTask.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    if sop_code:
        try:
            sop_enum = SOPCode(sop_code)
            query = query.where(SOPTask.sop_code == sop_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid SOP code: {sop_code}")
    
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return [SOPTaskResponse.model_validate(t) for t in tasks]

@router.post("/tasks")
async def create_sop_task(
    task: SOPTaskCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new SOP task
    """
    machine_id_int = None
    if task.machine_id:
        result = await db.execute(
            select(Machine).where(Machine.machine_id == task.machine_id)
        )
        machine = result.scalar_one_or_none()
        if machine:
            machine_id_int = machine.id
        else:
            raise HTTPException(status_code=404, detail=f"Machine {task.machine_id} not found")
    
    try:
        sop_code_enum = SOPCode(task.sop_code)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid SOP code: {task.sop_code}")
    
    new_task = SOPTask(
        machine_id=machine_id_int,
        sop_code=sop_code_enum,
        task_name=task.task_name,
        description=task.description,
        scheduled_date=task.scheduled_date,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        priority=task.priority,
        status=SOPTaskStatus.PENDING
    )
    
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    
    return SOPTaskResponse.model_validate(new_task)

@router.get("/tasks/{task_id}")
async def get_sop_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific SOP task"""
    result = await db.execute(
        select(SOPTask).where(SOPTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"SOP task {task_id} not found")
    
    return SOPTaskResponse.model_validate(task)

@router.post("/tasks/{task_id}/complete")
async def complete_sop_task(
    task_id: int,
    results: Optional[str] = None,
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Mark an SOP task as completed"""
    result = await db.execute(
        select(SOPTask).where(SOPTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"SOP task {task_id} not found")
    
    task.status = SOPTaskStatus.COMPLETED
    task.completed_at = datetime.utcnow()
    if results:
        task.results = results
    if notes:
        task.notes = notes
    
    await db.commit()
    
    return {"message": "SOP task completed", "task_id": task_id}











