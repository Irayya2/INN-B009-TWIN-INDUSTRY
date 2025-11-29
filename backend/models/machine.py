"""
Machine Model
Represents factory machines with their specifications and status
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database.connection import Base

class MachineStatus(str, enum.Enum):
    OPERATIONAL = "operational"
    WARNING = "warning"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"

class MachineType(str, enum.Enum):
    CNC_MILL = "cnc_mill"
    LATHE = "lathe"
    CONVEYOR = "conveyor"
    COMPRESSOR = "compressor"
    PUMP = "pump"
    MOTOR = "motor"
    FURNACE = "furnace"

class Machine(Base):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    machine_type = Column(Enum(MachineType), nullable=False)
    status = Column(Enum(MachineStatus), default=MachineStatus.OPERATIONAL)
    
    # Specifications
    max_rpm = Column(Float, nullable=True)
    max_temperature = Column(Float, nullable=True)
    max_vibration = Column(Float, nullable=True)
    max_load = Column(Float, nullable=True)
    
    # Health metrics
    health_score = Column(Float, default=100.0)  # 0-100
    fault_probability = Column(Float, default=0.0)  # 0-100
    anomaly_score = Column(Float, default=0.0)  # 0-100
    
    # Location and metadata
    location = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    manufacturer = Column(String(100), nullable=True)
    installation_date = Column(DateTime, nullable=True)
    
    # Cost metrics
    downtime_cost_per_hour = Column(Float, default=1000.0)  # ₹ or $
    last_maintenance_date = Column(DateTime, nullable=True)
    next_maintenance_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sensor_data = relationship("SensorData", back_populates="machine", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="machine", cascade="all, delete-orphan")
    maintenance_logs = relationship("MaintenanceLog", back_populates="machine", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Machine(id={self.id}, machine_id='{self.machine_id}', status='{self.status}')>"









