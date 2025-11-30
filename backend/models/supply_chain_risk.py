"""
Supply Chain Risk Model
Tracks risk assessments for supply chain continuity
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database.connection import Base

class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SupplyChainRisk(Base):
    __tablename__ = "supply_chain_risk"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True, index=True)
    spare_part_id = Column(Integer, ForeignKey("spare_parts.id"), nullable=True, index=True)
    
    # Risk assessment
    risk_level = Column(Enum(RiskLevel), nullable=False, default=RiskLevel.LOW)
    risk_score = Column(Float, nullable=False)  # 0-100
    
    # Predictions
    predicted_delay_days = Column(Float, nullable=True)  # AI model prediction
    stockout_probability = Column(Float, nullable=True)  # 0-100
    estimated_stockout_date = Column(DateTime(timezone=True), nullable=True)
    
    # Factors contributing to risk
    inventory_level = Column(Float, nullable=True)  # percentage of min stock
    supplier_reliability = Column(Float, nullable=True)
    lead_time_variance = Column(Float, nullable=True)  # days of variance
    demand_forecast = Column(Float, nullable=True)
    
    # Mitigation
    recommended_action = Column(Text, nullable=True)
    urgency = Column(String(20), nullable=True)  # low, medium, high
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    supplier = relationship("Supplier")
    spare_part = relationship("SparePart")
    
    def __repr__(self):
        return f"<SupplyChainRisk(id={self.id}, risk_level='{self.risk_level}', score={self.risk_score})>"











