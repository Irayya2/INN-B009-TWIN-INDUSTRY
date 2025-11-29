"""
SOP Task Model
Manages Standard Operating Procedure tasks and workflows
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database.connection import Base

class SOPTaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class SOPCode(str, enum.Enum):
    SOP_MAINT_01 = "SOP-MAINT-01"  # Daily Machine Health Check
    SOP_MAINT_02 = "SOP-MAINT-02"  # Predictive Maintenance Scheduling
    SOP_SC_04 = "SOP-SC-04"  # Spare Parts Inventory Check
    SOP_RISK_07 = "SOP-RISK-07"  # Downtime & Risk Assessment Report

class SOPTask(Base):
    __tablename__ = "sop_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True, index=True)
    
    sop_code = Column(Enum(SOPCode), nullable=False, index=True)
    task_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Status and scheduling
    status = Column(Enum(SOPTaskStatus), default=SOPTaskStatus.PENDING)
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    
    # Scheduling
    scheduled_date = Column(DateTime(timezone=True), nullable=False, index=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Assignment
    assigned_to = Column(String(100), nullable=True)
    created_by = Column(String(100), nullable=True)
    
    # Checklist (JSON string)
    checklist = Column(Text, nullable=True)  # JSON array of checklist items
    
    # Results and notes
    results = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Flags
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(50), nullable=True)  # daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    machine = relationship("Machine")
    
    def __repr__(self):
        return f"<SOPTask(id={self.id}, sop_code='{self.sop_code}', status='{self.status}')>"









