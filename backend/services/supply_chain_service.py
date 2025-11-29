"""
Supply Chain Service
Handles supply chain risk assessment and delay prediction
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from models.supply_chain_risk import SupplyChainRisk, RiskLevel
from models.spare_part import SparePart, PartStatus
from models.supplier import Supplier
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np

class SupplyChainService:
    """
    Industrial supply chain continuity and risk assessment service
    Uses predictive models for delay forecasting and stockout prediction
    """
    
    async def assess_risk(
        self,
        spare_part: SparePart,
        supplier: Optional[Supplier],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Comprehensive supply chain risk assessment
        Returns risk level, score, and predictions
        """
        # 1. Calculate inventory level percentage
        inventory_level = (spare_part.current_quantity / spare_part.min_quantity * 100) if spare_part.min_quantity > 0 else 0
        
        # 2. Get supplier metrics
        supplier_reliability = supplier.reliability_score if supplier else 50.0
        average_lead_time = supplier.average_lead_time_days if supplier else spare_part.lead_time_days
        on_time_delivery = supplier.on_time_delivery_rate if supplier else 80.0
        
        # 3. Predict delivery delay
        delay_prediction = await self._predict_delivery_delay_simple(
            supplier_reliability,
            average_lead_time,
            on_time_delivery
        )
        
        # 4. Calculate stockout probability
        stockout_prob = self._calculate_stockout_probability(
            spare_part.current_quantity,
            spare_part.min_quantity,
            average_lead_time,
            delay_prediction
        )
        
        # 5. Estimate stockout date
        stockout_date = self._estimate_stockout_date(
            spare_part.current_quantity,
            average_lead_time + delay_prediction
        )
        
        # 6. Calculate risk score (0-100)
        risk_score = self._calculate_risk_score(
            inventory_level,
            supplier_reliability,
            delay_prediction,
            stockout_prob,
            spare_part.status
        )
        
        # 7. Determine risk level
        risk_level = self._determine_risk_level(risk_score)
        
        # 8. Generate recommendations
        recommendations = self._generate_supply_chain_recommendations(
            risk_score,
            inventory_level,
            stockout_prob,
            delay_prediction,
            spare_part
        )
        
        # 9. Create or update risk record in database
        await self._update_risk_record(
            spare_part,
            supplier,
            risk_level,
            risk_score,
            delay_prediction,
            stockout_prob,
            stockout_date,
            inventory_level,
            supplier_reliability,
            db
        )
        
        return {
            "risk_level": risk_level.value,
            "risk_score": round(risk_score, 2),
            "predicted_delay_days": round(delay_prediction, 2),
            "stockout_probability": round(stockout_prob, 2),
            "estimated_stockout_date": stockout_date.isoformat() if stockout_date else None,
            "inventory_level_percent": round(inventory_level, 2),
            "supplier_reliability": round(supplier_reliability, 2),
            "recommended_action": recommendations[0] if recommendations else "Monitor inventory levels",
            "all_recommendations": recommendations
        }
    
    async def _predict_delivery_delay_simple(
        self,
        supplier_reliability: float,
        average_lead_time: float,
        on_time_delivery_rate: float
    ) -> float:
        """
        Simple delay prediction model
        In production, use Prophet or regression models with historical data
        """
        # Base delay based on reliability (lower reliability = higher delay)
        reliability_factor = (100 - supplier_reliability) / 100
        base_delay = reliability_factor * average_lead_time * 0.3
        
        # Add variance based on on-time delivery rate
        delivery_variance = (100 - on_time_delivery_rate) / 100 * average_lead_time * 0.2
        
        # Add random component (simulating real-world uncertainty)
        random_factor = np.random.uniform(-0.5, 1.0)
        
        total_delay = base_delay + delivery_variance + random_factor
        
        return max(0, total_delay)
    
    def _calculate_stockout_probability(
        self,
        current_quantity: int,
        min_quantity: int,
        lead_time_days: float,
        delay_days: float
    ) -> float:
        """
        Calculate probability of stockout
        Simplified model based on inventory levels and lead time
        """
        if current_quantity <= 0:
            return 100.0
        
        if current_quantity <= min_quantity:
            # Critical: already below minimum
            days_remaining = (current_quantity / min_quantity) * 7 if min_quantity > 0 else 0
            total_lead_time = lead_time_days + delay_days
            
            if days_remaining < total_lead_time:
                return min(100, 50 + (total_lead_time - days_remaining) * 10)
            else:
                return 30
        
        # Normal stock level
        buffer = (current_quantity - min_quantity) / min_quantity if min_quantity > 0 else 1
        
        if buffer < 0.5:  # Less than 50% buffer
            return 20 + (0.5 - buffer) * 40
        else:
            return max(0, 10 - buffer * 5)
    
    def _estimate_stockout_date(
        self,
        current_quantity: int,
        total_lead_time_days: float
    ) -> Optional[datetime]:
        """
        Estimate when stockout might occur
        Simplified: assumes constant consumption rate
        """
        if current_quantity <= 0:
            return datetime.utcnow()
        
        # Assume average consumption: reaches min_quantity in ~30 days for typical parts
        # This is a simplification - real models would use historical consumption data
        days_until_min = (current_quantity * 30) / 50  # Rough estimate
        
        if days_until_min < total_lead_time_days:
            return datetime.utcnow() + timedelta(days=days_until_min)
        
        return None
    
    def _calculate_risk_score(
        self,
        inventory_level: float,
        supplier_reliability: float,
        delay_prediction: float,
        stockout_probability: float,
        part_status: PartStatus
    ) -> float:
        """
        Calculate overall risk score (0-100)
        Higher score = higher risk
        """
        # Inventory risk component (0-40 points)
        if inventory_level <= 0:
            inventory_risk = 40
        elif inventory_level < 50:
            inventory_risk = 35
        elif inventory_level < 100:
            inventory_risk = 25
        elif inventory_level < 150:
            inventory_risk = 15
        else:
            inventory_risk = 5
        
        # Supplier reliability risk (0-30 points)
        supplier_risk = (100 - supplier_reliability) * 0.3
        
        # Delay risk (0-20 points)
        delay_risk = min(20, delay_prediction * 2)
        
        # Stockout probability risk (0-10 points)
        stockout_risk = stockout_probability * 0.1
        
        # Status penalty
        status_penalty = 0
        if part_status == PartStatus.OUT_OF_STOCK:
            status_penalty = 20
        elif part_status == PartStatus.LOW_STOCK:
            status_penalty = 10
        
        total_risk = inventory_risk + supplier_risk + delay_risk + stockout_risk + status_penalty
        
        return min(100.0, total_risk)
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Determine risk level from score"""
        if risk_score >= 70:
            return RiskLevel.CRITICAL
        elif risk_score >= 50:
            return RiskLevel.HIGH
        elif risk_score >= 30:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _generate_supply_chain_recommendations(
        self,
        risk_score: float,
        inventory_level: float,
        stockout_probability: float,
        delay_prediction: float,
        spare_part: SparePart
    ) -> list:
        """Generate actionable supply chain recommendations"""
        recommendations = []
        
        if risk_score >= 70:
            recommendations.append("URGENT: Place immediate order for spare parts")
            recommendations.append("Consider alternative suppliers")
            recommendations.append("Expedite delivery if possible")
        
        elif risk_score >= 50:
            recommendations.append("Place order before stock reaches minimum threshold")
            recommendations.append("Monitor supplier delivery status closely")
        
        if inventory_level < 100:
            order_quantity = max(spare_part.min_quantity * 2, spare_part.max_quantity * 0.5)
            recommendations.append(f"Consider ordering {int(order_quantity)} units")
        
        if delay_prediction > 3:
            recommendations.append(f"Account for expected delay of {delay_prediction:.1f} days in planning")
        
        if stockout_probability > 50:
            recommendations.append("Implement emergency procurement procedures")
            recommendations.append("Notify production planning team")
        
        if not recommendations:
            recommendations.append("Inventory levels are healthy")
            recommendations.append("Continue regular monitoring")
        
        return recommendations
    
    async def _update_risk_record(
        self,
        spare_part: SparePart,
        supplier: Optional[Supplier],
        risk_level: RiskLevel,
        risk_score: float,
        delay_prediction: float,
        stockout_probability: float,
        stockout_date: Optional[datetime],
        inventory_level: float,
        supplier_reliability: float,
        db: AsyncSession
    ):
        """Create or update risk record in database"""
        from sqlalchemy import select
        
        # Check if risk record exists
        result = await db.execute(
            select(SupplyChainRisk).where(SupplyChainRisk.spare_part_id == spare_part.id)
        )
        risk_record = result.scalar_one_or_none()
        
        recommendations = self._generate_supply_chain_recommendations(
            risk_score,
            inventory_level,
            stockout_probability,
            delay_prediction,
            spare_part
        )
        
        if risk_record:
            # Update existing record
            risk_record.risk_level = risk_level
            risk_record.risk_score = risk_score
            risk_record.predicted_delay_days = delay_prediction
            risk_record.stockout_probability = stockout_probability
            risk_record.estimated_stockout_date = stockout_date
            risk_record.inventory_level = inventory_level
            risk_record.supplier_reliability = supplier_reliability
            risk_record.recommended_action = recommendations[0] if recommendations else None
            risk_record.updated_at = datetime.utcnow()
        else:
            # Create new record
            risk_record = SupplyChainRisk(
                spare_part_id=spare_part.id,
                supplier_id=supplier.id if supplier else None,
                risk_level=risk_level,
                risk_score=risk_score,
                predicted_delay_days=delay_prediction,
                stockout_probability=stockout_probability,
                estimated_stockout_date=stockout_date,
                inventory_level=inventory_level,
                supplier_reliability=supplier_reliability,
                recommended_action=recommendations[0] if recommendations else None,
                urgency="high" if risk_score >= 70 else "medium" if risk_score >= 50 else "low"
            )
            db.add(risk_record)
        
        await db.commit()
    
    async def predict_delivery_delay(
        self,
        supplier: Supplier,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Predict delivery delay for a supplier
        In production, use Prophet or time-series regression with historical data
        """
        delay_days = await self._predict_delivery_delay_simple(
            supplier.reliability_score,
            supplier.average_lead_time_days,
            supplier.on_time_delivery_rate
        )
        
        return {
            "supplier_id": supplier.id,
            "supplier_name": supplier.name,
            "predicted_delay_days": round(delay_days, 2),
            "confidence": "medium",  # Would be calculated from model confidence
            "factors": [
                f"Reliability score: {supplier.reliability_score:.1f}",
                f"Average lead time: {supplier.average_lead_time_days:.1f} days",
                f"On-time delivery rate: {supplier.on_time_delivery_rate:.1f}%"
            ]
        }









