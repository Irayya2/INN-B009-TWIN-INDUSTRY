"""
Monitoring Service
Continuous monitoring of machines, generating alerts, and updating predictions
"""

import asyncio
import httpx
from datetime import datetime
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringService:
    """
    Industrial monitoring service that continuously:
    - Monitors machine health
    - Runs fault predictions
    - Generates alerts
    - Updates health scores
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.running = False
    
    async def start_monitoring(self, interval_seconds: int = 60):
        """Start continuous monitoring loop"""
        self.running = True
        logger.info(f"Starting monitoring service (interval: {interval_seconds}s)")
        
        while self.running:
            try:
                await self.run_monitoring_cycle()
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}", exc_info=True)
                await asyncio.sleep(interval_seconds)
    
    async def run_monitoring_cycle(self):
        """Execute one monitoring cycle"""
        logger.info("Running monitoring cycle...")
        
        async with httpx.AsyncClient() as client:
            # 1. Get all machines
            machines_response = await client.get(f"{self.api_base_url}/api/machines/")
            if machines_response.status_code != 200:
                logger.error(f"Failed to fetch machines: {machines_response.status_code}")
                return
            
            machines = machines_response.json()
            logger.info(f"Monitoring {len(machines)} machines")
            
            # 2. Run fault predictions for all machines
            predictions_response = await client.get(f"{self.api_base_url}/api/faults/predict/all")
            if predictions_response.status_code == 200:
                predictions = predictions_response.json()
                logger.info(f"Completed fault predictions for {len(predictions.get('predictions', []))} machines")
            
            # 3. Check for new alerts
            alerts_response = await client.get(f"{self.api_base_url}/api/alerts/active")
            if alerts_response.status_code == 200:
                alerts_data = alerts_response.json()
                active_count = alerts_data.get("count", 0)
                if active_count > 0:
                    logger.warning(f"Active alerts: {active_count}")
            
            # 4. Check supply chain risks
            risks_response = await client.get(f"{self.api_base_url}/api/supply/risk/all")
            if risks_response.status_code == 200:
                risks_data = risks_response.json()
                risks = risks_data.get("risks", [])
                critical_risks = [r for r in risks if r.get("risk_level") == "critical"]
                if critical_risks:
                    logger.warning(f"Critical supply chain risks: {len(critical_risks)}")
            
            logger.info("Monitoring cycle completed")
    
    def stop_monitoring(self):
        """Stop monitoring service"""
        self.running = False
        logger.info("Stopping monitoring service")

async def main():
    """Main entry point for monitoring service"""
    service = MonitoringService()
    try:
        await service.start_monitoring(interval_seconds=60)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        service.stop_monitoring()

if __name__ == "__main__":
    asyncio.run(main())











