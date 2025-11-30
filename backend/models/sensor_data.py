"""
Sensor Data Model
Stores real-time sensor readings from machines
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False, index=True)
    
    # Sensor readings
    vibration = Column(Float, nullable=False)  # mm/s or g
    temperature = Column(Float, nullable=False)  # Celsius
    acoustic_noise = Column(Float, nullable=False)  # dB
    load = Column(Float, nullable=False)  # percentage
    rpm = Column(Float, nullable=False)  # revolutions per minute
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Anomaly detection flags
    is_anomaly = Column(Integer, default=0)  # 0=normal, 1=anomaly
    anomaly_score = Column(Float, default=0.0)  # ML model output
    
    # Relationships
    machine = relationship("Machine", back_populates="sensor_data")
    
    # Index for efficient time-series queries
    __table_args__ = (
        Index('idx_machine_timestamp', 'machine_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<SensorData(machine_id={self.machine_id}, timestamp='{self.timestamp}')>"











