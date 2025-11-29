"""
Database Initialization Script
Creates sample data for testing the system
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path.parent))

from database.connection import Base, DATABASE_URL, init_db
from models.machine import Machine, MachineStatus, MachineType
from models.spare_part import SparePart, PartStatus
from models.supplier import Supplier
from models.alert import Alert, AlertType, AlertSeverity, AlertStatus

async def create_sample_data():
    """Create sample machines, suppliers, and spare parts"""
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Create machines
        machines_data = [
            {
                "machine_id": "CNC-001",
                "name": "CNC Milling Machine 001",
                "machine_type": MachineType.CNC_MILL,
                "max_rpm": 3000,
                "max_temperature": 80,
                "max_vibration": 10,
                "max_load": 100,
                "location": "Production Floor A",
                "department": "Manufacturing",
                "downtime_cost_per_hour": 1500.0
            },
            {
                "machine_id": "LATHE-002",
                "name": "Lathe Machine 002",
                "machine_type": MachineType.LATHE,
                "max_rpm": 2500,
                "max_temperature": 75,
                "max_vibration": 8,
                "max_load": 95,
                "location": "Production Floor B",
                "department": "Manufacturing",
                "downtime_cost_per_hour": 1200.0
            },
            {
                "machine_id": "CONV-003",
                "name": "Conveyor Belt 003",
                "machine_type": MachineType.CONVEYOR,
                "max_rpm": 500,
                "max_temperature": 60,
                "max_vibration": 5,
                "max_load": 80,
                "location": "Assembly Line 1",
                "department": "Assembly",
                "downtime_cost_per_hour": 800.0
            },
        ]
        
        for machine_data in machines_data:
            result = await session.execute(
                select(Machine).where(Machine.machine_id == machine_data["machine_id"])
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                machine = Machine(**machine_data, status=MachineStatus.OPERATIONAL)
                session.add(machine)
                print(f"Created machine: {machine_data['machine_id']}")
        
        # Create suppliers
        suppliers_data = [
            {
                "supplier_code": "SUP-001",
                "name": "Industrial Parts Co.",
                "contact_person": "John Smith",
                "email": "john@industrialparts.com",
                "phone": "+1-555-0101",
                "city": "Chicago",
                "country": "USA",
                "latitude": 41.8781,
                "longitude": -87.6298,
                "reliability_score": 92.0,
                "average_lead_time_days": 7.0,
                "on_time_delivery_rate": 95.0
            },
            {
                "supplier_code": "SUP-002",
                "name": "Global Components Ltd.",
                "contact_person": "Jane Doe",
                "email": "jane@globalcomponents.com",
                "phone": "+1-555-0102",
                "city": "New York",
                "country": "USA",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "reliability_score": 85.0,
                "average_lead_time_days": 10.0,
                "on_time_delivery_rate": 88.0
            },
        ]
        
        suppliers = []
        for supplier_data in suppliers_data:
            result = await session.execute(
                select(Supplier).where(Supplier.supplier_code == supplier_data["supplier_code"])
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                supplier = Supplier(**supplier_data)
                session.add(supplier)
                suppliers.append(supplier)
                print(f"Created supplier: {supplier_data['supplier_code']}")
        
        await session.flush()
        
        # Create spare parts
        if suppliers:
            spare_parts_data = [
                {
                    "part_number": "BEAR-001",
                    "name": "Bearing Assembly",
                    "description": "High-speed bearing assembly for CNC machines",
                    "current_quantity": 15,
                    "min_quantity": 5,
                    "max_quantity": 50,
                    "unit_cost": 125.0,
                    "primary_supplier_id": suppliers[0].id if suppliers else None,
                    "lead_time_days": 7,
                    "warehouse_location": "A-12-05"
                },
                {
                    "part_number": "BELT-002",
                    "name": "Conveyor Belt",
                    "description": "Heavy-duty conveyor belt",
                    "current_quantity": 8,
                    "min_quantity": 10,
                    "max_quantity": 30,
                    "unit_cost": 450.0,
                    "primary_supplier_id": suppliers[1].id if len(suppliers) > 1 else suppliers[0].id if suppliers else None,
                    "lead_time_days": 10,
                    "warehouse_location": "B-08-12"
                },
                {
                    "part_number": "MOTOR-003",
                    "name": "Electric Motor",
                    "description": "Industrial electric motor 5HP",
                    "current_quantity": 3,
                    "min_quantity": 5,
                    "max_quantity": 20,
                    "unit_cost": 850.0,
                    "primary_supplier_id": suppliers[0].id if suppliers else None,
                    "lead_time_days": 14,
                    "warehouse_location": "C-15-03"
                },
            ]
            
            for part_data in spare_parts_data:
                result = await session.execute(
                    select(SparePart).where(SparePart.part_number == part_data["part_number"])
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    part_data["total_value"] = part_data["current_quantity"] * part_data["unit_cost"]
                    if part_data["current_quantity"] <= 0:
                        part_data["status"] = PartStatus.OUT_OF_STOCK
                    elif part_data["current_quantity"] <= part_data["min_quantity"]:
                        part_data["status"] = PartStatus.LOW_STOCK
                    else:
                        part_data["status"] = PartStatus.IN_STOCK
                    
                    part = SparePart(**part_data)
                    session.add(part)
                    print(f"Created spare part: {part_data['part_number']}")
        
        await session.commit()
        print("\nSample data created successfully!")
    
    await engine.dispose()

async def main():
    """Main entry point"""
    try:
        print("Initializing database...")
        await init_db()
        print("\nCreating sample data...")
        await create_sample_data()
        print("\n✅ Setup complete! You can now start the backend server.")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        print("\nTroubleshooting:")
        print("1. Check PostgreSQL is running")
        print("2. Verify DATABASE_URL in backend/.env")
        print("3. Ensure database 'industrial_twin' exists")
        raise

if __name__ == "__main__":
    asyncio.run(main())

