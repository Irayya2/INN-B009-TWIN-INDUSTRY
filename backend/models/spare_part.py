"""
Spare Part Model
Manages inventory of spare parts
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database.connection import Base

class PartStatus(str, enum.Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    ON_ORDER = "on_order"
    DISCONTINUED = "discontinued"

class SparePart(Base):
    __tablename__ = "spare_parts"
    
    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Inventory
    current_quantity = Column(Integer, default=0, nullable=False)
    min_quantity = Column(Integer, default=5, nullable=False)  # Reorder point
    max_quantity = Column(Integer, default=50, nullable=False)
    unit = Column(String(20), default="pcs", nullable=False)
    
    # Cost
    unit_cost = Column(Float, nullable=False)
    total_value = Column(Float, default=0.0)  # current_quantity * unit_cost
    
    # Status
    status = Column(Enum(PartStatus), default=PartStatus.IN_STOCK)
    
    # Compatibility
    compatible_machines = Column(Text, nullable=True)  # JSON array of machine_ids
    
    # Supplier info
    primary_supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    lead_time_days = Column(Integer, default=7, nullable=False)  # Days to receive
    
    # Location
    warehouse_location = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_ordered_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="spare_parts")
    
    def __repr__(self):
        return f"<SparePart(id={self.id}, part_number='{self.part_number}', quantity={self.current_quantity})>"









