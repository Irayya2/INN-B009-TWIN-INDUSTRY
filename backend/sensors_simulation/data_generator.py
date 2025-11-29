"""
Sensor Data Generator Script
Generates and pushes synthetic sensor data to the API
"""

import asyncio
import httpx
import random
from datetime import datetime
from sensors_simulation.sensor_simulator import SensorSimulator, MultiMachineSimulator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SensorDataGenerator:
    """
    Continuously generates and pushes sensor data to the API
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.running = False
        
        # Default machine configurations
        self.machines_config = [
            {
                "machine_id": "CNC-001",
                "max_rpm": 3000,
                "max_temperature": 80,
                "max_vibration": 10,
                "max_load": 100
            },
            {
                "machine_id": "LATHE-002",
                "max_rpm": 2500,
                "max_temperature": 75,
                "max_vibration": 8,
                "max_load": 95
            },
            {
                "machine_id": "CONV-003",
                "max_rpm": 500,
                "max_temperature": 60,
                "max_vibration": 5,
                "max_load": 80
            }
        ]
        
        self.simulator = MultiMachineSimulator(self.machines_config)
    
    async def start_generating(self, interval_seconds: int = 5):
        """Start generating sensor data at regular intervals"""
        self.running = True
        logger.info(f"Starting sensor data generation (interval: {interval_seconds}s)")
        
        while self.running:
            try:
                await self.generate_and_push_data()
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Error generating sensor data: {e}", exc_info=True)
                await asyncio.sleep(interval_seconds)
    
    async def generate_and_push_data(self):
        """Generate sensor readings for all machines and push to API"""
        readings = self.simulator.generate_all_readings(inject_faults=False)
        
        async with httpx.AsyncClient() as client:
            for machine_id, reading in readings.items():
                try:
                    # Remove internal fields before sending
                    payload = {
                        "machine_id": reading["machine_id"],
                        "vibration": reading["vibration"],
                        "temperature": reading["temperature"],
                        "acoustic_noise": reading["acoustic_noise"],
                        "load": reading["load"],
                        "rpm": reading["rpm"]
                    }
                    
                    response = await client.post(
                        f"{self.api_base_url}/api/sensors/push",
                        json=payload,
                        timeout=5.0
                    )
                    
                    if response.status_code == 200:
                        logger.debug(f"Pushed sensor data for {machine_id}")
                    else:
                        logger.warning(f"Failed to push data for {machine_id}: {response.status_code}")
                
                except Exception as e:
                    logger.error(f"Error pushing data for {machine_id}: {e}")
    
    def stop_generating(self):
        """Stop generating sensor data"""
        self.running = False
        logger.info("Stopping sensor data generation")

async def main():
    """Main entry point"""
    generator = SensorDataGenerator()
    try:
        await generator.start_generating(interval_seconds=5)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        generator.stop_generating()

if __name__ == "__main__":
    asyncio.run(main())

