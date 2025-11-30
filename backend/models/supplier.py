"""
Supplier Model
Stores supplier information and performance metrics
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    
    # Contact information
    contact_person = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    
    # Location
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)  # For map visualization
    longitude = Column(Float, nullable=True)
    
    # Performance metrics
    reliability_score = Column(Float, default=100.0)  # 0-100
    average_lead_time_days = Column(Float, default=7.0)
    on_time_delivery_rate = Column(Float, default=95.0)  # percentage
    
    # Financial
    total_orders = Column(Integer, default=0)
    total_value = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Integer, default=1)  # 1=active, 0=inactive
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    spare_parts = relationship("SparePart", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.name}', reliability={self.reliability_score})>"











