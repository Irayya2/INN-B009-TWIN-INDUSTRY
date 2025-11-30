"""
Maintenance Log Model
Tracks maintenance activities and history
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database.connection import Base

class MaintenanceType(str, enum.Enum):
    PREVENTIVE = "preventive"
    PREDICTIVE = "predictive"
    CORRECTIVE = "corrective"
    EMERGENCY = "emergency"

class MaintenanceStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False, index=True)
    
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    status = Column(Enum(MaintenanceStatus), default=MaintenanceStatus.SCHEDULED)
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Scheduling
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_hours = Column(Float, nullable=True)
    
    # Cost and resources
    cost = Column(Float, nullable=True)
    technician = Column(String(100), nullable=True)
    spare_parts_used = Column(Text, nullable=True)  # JSON string of parts
    
    # SOP reference
    sop_reference = Column(String(50), nullable=True)  # e.g., "SOP-MAINT-02"
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    machine = relationship("Machine", back_populates="maintenance_logs")
    
    def __repr__(self):
        return f"<MaintenanceLog(id={self.id}, type='{self.maintenance_type}', status='{self.status}')>"











