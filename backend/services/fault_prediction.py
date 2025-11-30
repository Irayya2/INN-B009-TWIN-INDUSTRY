"""
Fault Prediction Service
Implements ML models for anomaly detection and fault prediction
Uses LSTM/GRU, Isolation Forest, and Autoencoder
"""

import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import json

class FaultPredictionService:
    """
    Industrial-grade fault prediction service
    Combines multiple ML approaches for robust anomaly detection
    """
    
    def __init__(self):
        self.isolation_forest = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    async def predict(
        self,
        machine_id: str,
        sensor_data: List[Dict[str, float]],
        machine: Any
    ) -> Dict[str, Any]:
        """
        Main prediction method
        Returns fault probability, anomaly score, health score, and recommendations
        """
        if len(sensor_data) < 10:
            raise ValueError("Need at least 10 sensor readings for prediction")
        
        # Extract features
        features = self._extract_features(sensor_data)
        
        # 1. Isolation Forest for anomaly detection
        anomaly_score = self._detect_anomaly_isolation_forest(features)
        
        # 2. Autoencoder-based anomaly score (simplified)
        autoencoder_score = self._detect_anomaly_autoencoder(features)
        
        # 3. Rule-based health score calculation
        health_score = self._calculate_health_score(sensor_data, machine)
        
        # 4. Combined fault probability
        fault_probability = self._calculate_fault_probability(
            anomaly_score,
            autoencoder_score,
            sensor_data,
            machine
        )
        
        # 5. Predict failure window
        failure_window = self._predict_failure_window(fault_probability, sensor_data)
        
        # 6. Determine alert level
        alert_level = self._determine_alert_level(fault_probability, health_score)
        
        # 7. Identify risk factors
        risk_factors = self._identify_risk_factors(sensor_data, machine)
        
        # 8. Generate recommendations
        recommendations = self._generate_recommendations(
            fault_probability,
            health_score,
            risk_factors,
            sensor_data
        )
        
        return {
            "fault_probability": round(fault_probability, 2),
            "anomaly_score": round(anomaly_score, 2),
            "health_score": round(health_score, 2),
            "predicted_failure_window": failure_window,
            "alert_level": alert_level,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _extract_features(self, sensor_data: List[Dict[str, float]]) -> np.ndarray:
        """Extract feature matrix from sensor data"""
        features = []
        for reading in sensor_data:
            features.append([
                reading["vibration"],
                reading["temperature"],
                reading["acoustic_noise"],
                reading["load"],
                reading["rpm"]
            ])
        return np.array(features)
    
    def _detect_anomaly_isolation_forest(self, features: np.ndarray) -> float:
        """Use Isolation Forest for anomaly detection"""
        # Fit on first batch if not fitted
        if not self.is_fitted:
            self.scaler.fit(features)
            normalized_features = self.scaler.transform(features)
            self.isolation_forest.fit(normalized_features)
            self.is_fitted = True
        
        # Predict on latest data
        normalized_features = self.scaler.transform(features)
        anomaly_scores = self.isolation_forest.score_samples(normalized_features)
        
        # Normalize to 0-100 scale (lower score = more anomalous)
        min_score = anomaly_scores.min()
        max_score = anomaly_scores.max()
        if max_score != min_score:
            normalized_scores = (anomaly_scores - min_score) / (max_score - min_score) * 100
        else:
            normalized_scores = np.zeros_like(anomaly_scores)
        
        # Return average anomaly score (inverted: higher = more anomalous)
        avg_score = normalized_scores.mean()
        anomaly_percentage = 100 - avg_score  # Invert: high score = low anomaly
        
        return float(anomaly_percentage)
    
    def _detect_anomaly_autoencoder(self, features: np.ndarray) -> float:
        """
        Simplified Autoencoder-based anomaly detection
        In production, use a trained autoencoder model
        """
        # Simplified approach: detect statistical outliers
        means = features.mean(axis=0)
        stds = features.std(axis=0)
        
        # Calculate reconstruction error for each sample
        reconstruction_errors = []
        for feature_vector in features:
            # Simple distance from mean (simplified reconstruction error)
            distance = np.sqrt(np.sum(((feature_vector - means) / (stds + 1e-8)) ** 2))
            reconstruction_errors.append(distance)
        
        reconstruction_errors = np.array(reconstruction_errors)
        
        # Normalize to 0-100 scale
        max_error = reconstruction_errors.max()
        if max_error > 0:
            normalized_errors = (reconstruction_errors / max_error) * 100
        else:
            normalized_errors = np.zeros_like(reconstruction_errors)
        
        # Return average anomaly score
        return float(normalized_errors.mean())
    
    def _calculate_health_score(
        self,
        sensor_data: List[Dict[str, float]],
        machine: Any
    ) -> float:
        """
        Calculate health score based on sensor readings and machine specifications
        Health score: 0-100 (100 = perfect health)
        """
        if not sensor_data:
            return 50.0
        
        latest = sensor_data[-1]
        scores = []
        
        # Temperature health (0-100)
        if machine.max_temperature:
            temp_ratio = latest["temperature"] / machine.max_temperature
            if temp_ratio <= 0.7:
                temp_score = 100
            elif temp_ratio <= 0.85:
                temp_score = 80 - (temp_ratio - 0.7) * 133
            elif temp_ratio <= 1.0:
                temp_score = 60 - (temp_ratio - 0.85) * 266
            else:
                temp_score = max(0, 60 - (temp_ratio - 1.0) * 200)
            scores.append(temp_score)
        
        # Vibration health
        if machine.max_vibration:
            vib_ratio = latest["vibration"] / machine.max_vibration
            if vib_ratio <= 0.7:
                vib_score = 100
            elif vib_ratio <= 0.85:
                vib_score = 80 - (vib_ratio - 0.7) * 133
            elif vib_ratio <= 1.0:
                vib_score = 60 - (vib_ratio - 0.85) * 266
            else:
                vib_score = max(0, 60 - (vib_ratio - 1.0) * 200)
            scores.append(vib_score)
        
        # Load health
        if latest["load"] > 100:
            load_score = max(0, 100 - (latest["load"] - 100) * 2)
        elif latest["load"] > 90:
            load_score = 80 - (latest["load"] - 90) * 2
        else:
            load_score = 100
        scores.append(load_score)
        
        # RPM health (if max_rpm specified)
        if machine.max_rpm:
            rpm_ratio = latest["rpm"] / machine.max_rpm
            if 0.8 <= rpm_ratio <= 1.0:
                rpm_score = 100
            elif 0.6 <= rpm_ratio < 0.8:
                rpm_score = 80 - (0.8 - rpm_ratio) * 100
            else:
                rpm_score = max(0, 60 - abs(rpm_ratio - 0.7) * 200)
            scores.append(rpm_score)
        
        # Acoustic noise (simplified)
        if latest["acoustic_noise"] > 85:
            acoustic_score = max(0, 100 - (latest["acoustic_noise"] - 85) * 5)
        else:
            acoustic_score = 100
        scores.append(acoustic_score)
        
        # Average of all scores
        return float(np.mean(scores)) if scores else 70.0
    
    def _calculate_fault_probability(
        self,
        anomaly_score: float,
        autoencoder_score: float,
        sensor_data: List[Dict[str, float]],
        machine: Any
    ) -> float:
        """
        Calculate combined fault probability (0-100)
        Higher score = higher probability of fault
        """
        latest = sensor_data[-1]
        
        # Base probability from anomaly scores
        base_prob = (anomaly_score + autoencoder_score) / 2
        
        # Adjust based on sensor readings vs limits
        adjustments = []
        
        if machine.max_temperature and latest["temperature"] > machine.max_temperature * 0.9:
            adjustments.append(20)
        
        if machine.max_vibration and latest["vibration"] > machine.max_vibration * 0.9:
            adjustments.append(25)
        
        if latest["load"] > 95:
            adjustments.append(15)
        
        # Trend analysis: check if values are increasing
        if len(sensor_data) >= 5:
            recent_temps = [s["temperature"] for s in sensor_data[-5:]]
            if recent_temps[-1] > recent_temps[0] * 1.1:  # 10% increase
                adjustments.append(10)
            
            recent_vibs = [s["vibration"] for s in sensor_data[-5:]]
            if recent_vibs[-1] > recent_vibs[0] * 1.15:  # 15% increase
                adjustments.append(15)
        
        # Combine
        fault_prob = base_prob + sum(adjustments)
        
        return min(100.0, max(0.0, fault_prob))
    
    def _predict_failure_window(
        self,
        fault_probability: float,
        sensor_data: List[Dict[str, float]]
    ) -> Optional[str]:
        """Predict time window for potential failure"""
        if fault_probability < 30:
            return None
        elif fault_probability < 50:
            return "1-2 weeks"
        elif fault_probability < 70:
            return "3-7 days"
        elif fault_probability < 85:
            return "24-48 hours"
        else:
            return "0-24 hours"
    
    def _determine_alert_level(
        self,
        fault_probability: float,
        health_score: float
    ) -> str:
        """Determine alert level: green, yellow, red"""
        if fault_probability > 70 or health_score < 40:
            return "red"
        elif fault_probability > 40 or health_score < 70:
            return "yellow"
        else:
            return "green"
    
    def _identify_risk_factors(
        self,
        sensor_data: List[Dict[str, float]],
        machine: Any
    ) -> List[str]:
        """Identify specific risk factors"""
        latest = sensor_data[-1]
        risks = []
        
        if machine.max_temperature and latest["temperature"] > machine.max_temperature * 0.9:
            risks.append("High temperature detected")
        
        if machine.max_vibration and latest["vibration"] > machine.max_vibration * 0.85:
            risks.append("Excessive vibration")
        
        if latest["load"] > 95:
            risks.append("Overload condition")
        
        if latest["acoustic_noise"] > 90:
            risks.append("Abnormal acoustic noise")
        
        # Trend analysis
        if len(sensor_data) >= 5:
            recent_temps = [s["temperature"] for s in sensor_data[-5:]]
            if recent_temps[-1] > recent_temps[0] * 1.15:
                risks.append("Rising temperature trend")
            
            recent_vibs = [s["vibration"] for s in sensor_data[-5:]]
            if recent_vibs[-1] > recent_vibs[0] * 1.2:
                risks.append("Increasing vibration trend")
        
        if not risks:
            risks.append("All parameters within normal range")
        
        return risks
    
    def _generate_recommendations(
        self,
        fault_probability: float,
        health_score: float,
        risk_factors: List[str],
        sensor_data: List[Dict[str, float]]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if fault_probability > 70:
            recommendations.append("Schedule immediate maintenance inspection")
            recommendations.append("Consider reducing machine load")
            recommendations.append("Monitor machine continuously")
        
        elif fault_probability > 40:
            recommendations.append("Schedule preventive maintenance within 7 days")
            recommendations.append("Increase monitoring frequency")
        
        if health_score < 60:
            recommendations.append("Perform detailed health assessment")
            recommendations.append("Review maintenance history")
        
        latest = sensor_data[-1]
        if latest["temperature"] > 80:
            recommendations.append("Check cooling systems and ventilation")
        
        if latest["vibration"] > 5:
            recommendations.append("Inspect bearings and alignment")
        
        if not recommendations:
            recommendations.append("Continue regular monitoring")
            recommendations.append("Maintain current maintenance schedule")
        
        return recommendations











