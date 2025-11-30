# AI-Driven Industrial Twin for Predictive Maintenance and Supply Chain Continuity

A comprehensive, industry-grade software system for simulating manufacturing factories, predicting machine failures using AI, monitoring equipment health in real-time, and forecasting supply chain risks.

## 🔵 System Overview

This system combines:
- **Real-time sensor data simulation** (vibration, temperature, acoustic noise, load, RPM)
- **AI-powered fault prediction** (LSTM/GRU, Isolation Forest, Autoencoder)
- **Supply chain risk assessment** (delay prediction, stockout forecasting)
- **Industrial SOP workflows** (maintenance scheduling, inventory checks)
- **Real-time dashboards** (React frontend with live charts)

## 🏗️ Architecture

### Backend (Python FastAPI)
```
backend/
├── main.py                 # FastAPI application entry point
├── api/                    # API routes
├── models/                 # Database models (SQLAlchemy)
├── database/               # Database connection and setup
├── services/               # Business logic services
│   ├── fault_prediction.py    # ML fault prediction
│   └── supply_chain_service.py # Supply chain risk assessment
├── sensors_simulation/     # Sensor data generation
├── monitoring/             # Background monitoring service
└── ml_models/             # ML model training and inference
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   ├── pages/            # Main application pages
│   ├── charts/           # Chart components (Recharts)
│   ├── hooks/            # Custom React hooks
│   └── services/         # API client services
```

### Database (PostgreSQL)
- `machines` - Machine specifications and status
- `sensor_data` - Real-time sensor readings
- `alerts` - System alerts and warnings
- `maintenance_logs` - Maintenance history
- `spare_parts` - Inventory management
- `suppliers` - Supplier information
- `supply_chain_risk` - Risk assessments
- `sop_tasks` - SOP workflow tasks

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- npm or yarn

### Backend Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up database:**
```bash
# Create PostgreSQL database
createdb industrial_twin

# Update .env file with database credentials
cp .env.example .env
# Edit .env with your database URL
```

3. **Run database migrations:**
The database tables will be created automatically on first run.

4. **Start the API server:**
```bash
python main.py
# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. **Start sensor data generator (in a separate terminal):**
```bash
cd backend/sensors_simulation
python data_generator.py
```

6. **Start monitoring service (optional, in a separate terminal):**
```bash
cd backend/monitoring
python monitoring_service.py
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
# or
yarn install
```

2. **Start development server:**
```bash
npm run dev
# or
yarn dev
```

3. **Access the application:**
Open http://localhost:5173 in your browser

## 📡 API Endpoints

### Sensors
- `POST /api/sensors/push` - Store live sensor data
- `GET /api/sensors/latest/{machine_id}` - Get latest sensor readings
- `GET /api/sensors/timeframe/{machine_id}` - Get sensor data for time window

### Machines
- `GET /api/machines/` - Get all machines
- `GET /api/machines/{machine_id}` - Get machine status
- `GET /api/machines/status/all` - Get all machines status overview

### Fault Prediction
- `GET /api/faults/predict/{machine_id}` - Get ML fault prediction
- `GET /api/faults/predict/all` - Get predictions for all machines

### Supply Chain
- `GET /api/supply/risk/{part_id}` - Get supply chain risk assessment
- `GET /api/supply/risk/all` - Get all supply chain risks
- `GET /api/supply/delay-prediction/{supplier_id}` - Predict delivery delays

### Inventory
- `GET /api/inventory/check` - Check inventory status (SOP-SC-04)
- `GET /api/inventory/{part_id}` - Get spare part details

### Alerts
- `GET /api/alerts/` - Get all alerts
- `GET /api/alerts/active` - Get active alerts
- `POST /api/alerts/{alert_id}/acknowledge` - Acknowledge alert
- `POST /api/alerts/{alert_id}/resolve` - Resolve alert

### SOP Tasks
- `GET /api/sop/tasks` - Get all SOP tasks
- `POST /api/sop/tasks` - Create SOP task
- `POST /api/sop/tasks/{task_id}/complete` - Complete SOP task

### Maintenance
- `POST /api/maintenance/schedule` - Schedule maintenance (SOP-MAINT-02)
- `GET /api/maintenance/logs` - Get maintenance logs

## 🔵 SOP Workflows

The system implements the following Standard Operating Procedures:

1. **SOP-MAINT-01**: Daily Machine Health Check
2. **SOP-MAINT-02**: Predictive Maintenance Scheduling
3. **SOP-SC-04**: Spare Parts Inventory Check
4. **SOP-RISK-07**: Downtime & Risk Assessment Report

## 🤖 ML Models

### Fault Prediction
- **Isolation Forest**: Anomaly detection from sensor patterns
- **Autoencoder**: Reconstruction error-based anomaly scoring
- **Health Score Calculation**: Rule-based health assessment
- **Failure Window Prediction**: Time-to-failure estimation

### Supply Chain Risk
- **Delay Prediction**: Supplier reliability and lead time analysis
- **Stockout Probability**: Inventory level and consumption forecasting
- **Risk Scoring**: Multi-factor risk assessment

## 📊 Features

### Real-time Monitoring
- Live sensor data visualization
- Health score indicators
- Fault probability meters
- Alert notifications

### Predictive Maintenance
- Anomaly detection
- Failure window prediction
- Maintenance scheduling
- Cost analysis

### Supply Chain Continuity
- Delivery delay prediction
- Stockout forecasting
- Supplier reliability scoring
- Inventory optimization

### Industrial Workflows
- SOP task management
- Maintenance logs
- Incident reporting
- Cost tracking

## 🛠️ Development

### Running Tests
```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Structure
- Backend follows FastAPI best practices with async/await
- Frontend uses React hooks and functional components
- Database models use SQLAlchemy async ORM
- ML models are modular and extensible

## 📝 License

This project is proprietary software for industrial use.

## 🤝 Contributing

This is an internal industrial system. Contact the development team for contribution guidelines.

## 📞 Support

For issues and questions, contact the system administrator.











