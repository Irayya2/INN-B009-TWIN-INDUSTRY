"""
Sensor Data Simulator
Generates realistic synthetic sensor data for factory machines
Simulates: vibration, temperature, acoustic noise, load, RPM
"""

import numpy as np
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random
import math

class SensorSimulator:
    """
    Industrial sensor data simulator
    Generates realistic sensor readings with fault patterns
    """
    
    def __init__(self, machine_id: str, config: Optional[Dict] = None):
        self.machine_id = machine_id
        self.config = config or {}
        
        # Machine specifications (defaults)
        self.max_rpm = self.config.get("max_rpm", 3000)
        self.max_temperature = self.config.get("max_temperature", 80)
        self.max_vibration = self.config.get("max_vibration", 10)
        self.max_load = self.config.get("max_load", 100)
        
        # State variables for realistic patterns
        self.base_temperature = 40.0
        self.base_vibration = 2.0
        self.time_counter = 0
        self.fault_mode = "normal"  # normal, bearing_wear, overheating, misalignment
        
        # Fault parameters
        self.fault_start_time = None
        self.fault_severity = 0.0
    
    def generate_reading(self, inject_fault: bool = False) -> Dict[str, float]:
        """
        Generate a single sensor reading
        Uses realistic patterns: sine waves for vibration, random walk for temperature
        """
        self.time_counter += 1
        
        # Determine fault mode
        if inject_fault:
            if self.fault_mode == "normal":
                self.fault_mode = random.choice(["bearing_wear", "overheating", "misalignment"])
                self.fault_start_time = self.time_counter
                self.fault_severity = random.uniform(0.3, 0.8)
        
        # Calculate fault progression
        fault_progression = 0.0
        if self.fault_mode != "normal" and self.fault_start_time:
            time_since_fault = self.time_counter - self.fault_start_time
            fault_progression = min(1.0, time_since_fault / 100)  # Gradual progression
        
        # 1. VIBRATION (mm/s or g)
        # Normal: sine wave with small noise
        # Bearing wear: gradual increase with spikes
        # Misalignment: higher baseline with periodic spikes
        if self.fault_mode == "bearing_wear":
            base_vib = self.base_vibration * (1 + fault_progression * 2)
            vibration = base_vib + 2 * math.sin(self.time_counter * 0.1) + \
                       random.gauss(0, 0.5) + fault_progression * 3 * random.random()
        elif self.fault_mode == "misalignment":
            vibration = self.base_vibration * 1.5 + 3 * math.sin(self.time_counter * 0.05) + \
                       random.gauss(0, 0.8)
        else:
            vibration = self.base_vibration + 0.5 * math.sin(self.time_counter * 0.1) + \
                       random.gauss(0, 0.3)
        
        vibration = max(0, min(vibration, self.max_vibration * 1.5))
        
        # 2. TEMPERATURE (Celsius)
        # Normal: random walk around base temperature
        # Overheating: gradual increase with occasional spikes
        temp_drift = random.gauss(0, 0.5)
        self.base_temperature += temp_drift * 0.1  # Slow drift
        
        if self.fault_mode == "overheating":
            temp_increase = fault_progression * 20 + 5 * random.random()
            temperature = self.base_temperature + temp_increase
        else:
            temperature = self.base_temperature + random.gauss(0, 2)
        
        # Keep within bounds
        temperature = max(20, min(temperature, self.max_temperature * 1.3))
        
        # 3. ACOUSTIC NOISE (dB)
        # Correlated with vibration
        acoustic_base = 60 + vibration * 3
        if self.fault_mode == "bearing_wear":
            acoustic_noise = acoustic_base + fault_progression * 15 + random.gauss(0, 2)
        else:
            acoustic_noise = acoustic_base + random.gauss(0, 1.5)
        
        acoustic_noise = max(50, min(acoustic_noise, 100))
        
        # 4. LOAD (percentage)
        # Normal operation: 70-90% with variations
        if self.fault_mode == "normal":
            load = random.uniform(70, 90) + random.gauss(0, 3)
        else:
            # Fault might cause load variations
            load = random.uniform(75, 95) + random.gauss(0, 5)
        
        load = max(0, min(load, self.max_load))
        
        # 5. RPM (revolutions per minute)
        # Normal: near max_rpm with small variations
        # Fault: might cause RPM fluctuations
        if self.fault_mode in ["bearing_wear", "misalignment"]:
            rpm_variation = fault_progression * 100
            rpm = self.max_rpm * 0.85 + random.gauss(0, 20) + rpm_variation * random.uniform(-0.5, 0.5)
        else:
            rpm = self.max_rpm * 0.85 + random.gauss(0, 15)
        
        rpm = max(0, min(rpm, self.max_rpm * 1.1))
        
        return {
            "machine_id": self.machine_id,
            "vibration": round(vibration, 2),
            "temperature": round(temperature, 2),
            "acoustic_noise": round(acoustic_noise, 2),
            "load": round(load, 2),
            "rpm": round(rpm, 2),
            "timestamp": datetime.utcnow(),
            "fault_mode": self.fault_mode
        }
    
    def generate_readings(self, count: int, inject_fault: bool = False) -> List[Dict[str, float]]:
        """Generate multiple sensor readings"""
        readings = []
        for i in range(count):
            # Inject fault after some readings
            should_inject = inject_fault and i > count * 0.6 and self.fault_mode == "normal"
            reading = self.generate_reading(inject_fault=should_inject)
            readings.append(reading)
        return readings
    
    def reset(self):
        """Reset simulator state"""
        self.time_counter = 0
        self.fault_mode = "normal"
        self.fault_start_time = None
        self.fault_severity = 0.0
        self.base_temperature = 40.0
        self.base_vibration = 2.0

class MultiMachineSimulator:
    """Simulate multiple machines simultaneously"""
    
    def __init__(self, machines_config: List[Dict]):
        self.simulators = {}
        for machine_config in machines_config:
            machine_id = machine_config["machine_id"]
            self.simulators[machine_id] = SensorSimulator(machine_id, machine_config)
    
    def generate_all_readings(self, inject_faults: bool = False) -> Dict[str, Dict[str, float]]:
        """Generate readings for all machines"""
        readings = {}
        for machine_id, simulator in self.simulators.items():
            readings[machine_id] = simulator.generate_reading(inject_fault=inject_faults)
        return readings
    
    def reset_all(self):
        """Reset all simulators"""
        for simulator in self.simulators.values():
            simulator.reset()









