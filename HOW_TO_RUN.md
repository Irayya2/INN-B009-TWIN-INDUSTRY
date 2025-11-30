# 🚀 How to Run the Industrial Twin System

## Quick Start Guide

This guide will walk you through running the complete system step by step.

---

## Prerequisites Check

Before starting, ensure you have:

- ✅ **Python 3.10+** installed
- ✅ **Node.js 18+** installed  
- ✅ **PostgreSQL 14+** installed and running
- ✅ **Git** (optional)

**Verify installations:**
```bash
python --version    # Should be 3.10 or higher
node --version      # Should be 18 or higher
psql --version      # Should be 14 or higher
```

---

## Step 1: Database Setup

### 1.1 Create PostgreSQL Database

```bash
# On Windows (Command Prompt or PowerShell)
createdb industrial_twin

# On macOS/Linux
sudo -u postgres createdb industrial_twin

# Or using psql:
psql -U postgres
CREATE DATABASE industrial_twin;
\q
```

### 1.2 Configure Database Connection

Create the environment file:

```bash
# Navigate to backend directory
cd backend

# Create .env file (Windows)
copy .env.example .env

# Create .env file (macOS/Linux)
cp .env.example .env
```

Edit `backend/.env` and update with your database credentials:

```env
DATABASE_URL=postgresql+asyncpg://your_username:your_password@localhost:5432/industrial_twin
```

**Example:**
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/industrial_twin
```

---

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 2.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- SQLAlchemy
- scikit-learn
- numpy
- and other required packages

### 2.4 Initialize Database with Sample Data

```bash
# From project root directory (go back one level)
cd ..
python scripts/init_db.py
```

**Expected Output:**
```
Initializing database...
Database initialized successfully
Creating sample data...
Created machine: CNC-001
Created machine: LATHE-002
Created machine: CONV-003
Created supplier: SUP-001
Created supplier: SUP-002
Created spare part: BEAR-001
Created spare part: BELT-002
Created spare part: MOTOR-003

Sample data created successfully!
```

### 2.5 Start the Backend Server

**Option 1: Using main.py (Recommended)**
```bash
cd backend
python main.py
```

**Option 2: Using uvicorn directly**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
Database initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Verify Backend:**
- Open browser: http://localhost:8000
- Should see: `{"message":"Industrial Twin API","status":"operational","version":"1.0.0"}`
- API Docs: http://localhost:8000/docs

**✅ Backend is now running! Keep this terminal open.**

---

## Step 3: Frontend Setup

### 3.1 Open a New Terminal

Keep the backend running and open a **new terminal window**.

### 3.2 Navigate to Frontend Directory

```bash
cd frontend
```

### 3.3 Install Node.js Dependencies

```bash
npm install
# or
yarn install
```

This will install:
- React
- Vite
- Recharts
- Axios
- React Router

### 3.4 Start Frontend Development Server

```bash
npm run dev
# or
yarn dev
```

**Expected Output:**
```
  VITE v5.0.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Verify Frontend:**
- Open browser: http://localhost:5173
- You should see the Industrial Twin dashboard

**✅ Frontend is now running! Keep this terminal open.**

---

## Step 4: Generate Sensor Data (Optional but Recommended)

### 4.1 Open Another Terminal

Keep both backend and frontend running.

### 4.2 Start Sensor Data Generator

```bash
cd backend/sensors_simulation
python data_generator.py
```

**Expected Output:**
```
INFO:__main__:Starting sensor data generation (interval: 5s)
INFO:__main__:Pushed sensor data for CNC-001
INFO:__main__:Pushed sensor data for LATHE-002
INFO:__main__:Pushed sensor data for CONV-003
```

This will continuously generate sensor data every 5 seconds for all machines.

**✅ Sensor data is now being generated!**

---

## Step 5: Start Monitoring Service (Optional)

### 5.1 Open Yet Another Terminal

### 5.2 Start Monitoring Service

```bash
cd backend/monitoring
python monitoring_service.py
```

**Expected Output:**
```
INFO:__main__:Starting monitoring service (interval: 60s)
INFO:__main__:Running monitoring cycle...
INFO:__main__:Monitoring 3 machines
INFO:__main__:Completed fault predictions for 3 machines
INFO:__main__:Monitoring cycle completed
```

This service runs predictions and generates alerts every 60 seconds.

**✅ Monitoring service is now running!**

---

## 📊 System Status

You should now have **4 terminals running**:

1. ✅ **Backend API** - Port 8000
2. ✅ **Frontend** - Port 5173  
3. ✅ **Sensor Generator** - Generating data
4. ✅ **Monitoring Service** - Running predictions

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend Dashboard** | http://localhost:5173 | Main application interface |
| **Backend API** | http://localhost:8000 | API root endpoint |
| **API Documentation** | http://localhost:8000/docs | Swagger UI for API testing |
| **Health Check** | http://localhost:8000/api/health | API health status |

---

## 🧪 Testing the System

### 1. View Dashboard
- Open: http://localhost:5173
- You should see machine overview, charts, and alerts

### 2. Check Machine Health
- Navigate to "Machine Health" page
- Select a machine (CNC-001, LATHE-002, or CONV-003)
- View real-time sensor data charts
- See health scores and fault predictions

### 3. View Supply Chain
- Navigate to "Supply Chain" page
- See risk assessments for spare parts
- Check inventory levels

### 4. Check Alerts
- Navigate to "Alerts" page
- View active alerts (if any)
- Test acknowledge/resolve functionality

### 5. Test API Endpoints
- Open: http://localhost:8000/docs
- Try endpoints interactively
- Example: GET `/api/machines/` - Get all machines

---

## 🔧 Troubleshooting

### Problem: Database Connection Error

**Error:** `connection refused` or `authentication failed`

**Solution:**
1. Verify PostgreSQL is running:
   ```bash
   # Windows
   services.msc  # Check PostgreSQL service
   
   # macOS/Linux
   sudo systemctl status postgresql
   ```

2. Check database credentials in `backend/.env`

3. Test connection:
   ```bash
   psql -U your_username -d industrial_twin
   ```

### Problem: Port Already in Use

**Error:** `Address already in use` on port 8000 or 5173

**Solution:**
- **Port 8000 (Backend):** Change port in `backend/main.py`:
  ```python
  port=8001  # Change from 8000
  ```

- **Port 5173 (Frontend):** Change port in `frontend/vite.config.js`:
  ```javascript
  server: {
    port: 5174,  // Change from 5173
  }
  ```

### Problem: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Problem: Frontend Can't Connect to Backend

**Error:** `Network Error` or `CORS error`

**Solution:**
1. Verify backend is running on port 8000
2. Check `frontend/src/services/api.js` - API URL should be `http://localhost:8000/api`
3. Verify CORS settings in `backend/main.py`

### Problem: No Sensor Data Showing

**Solution:**
1. Verify sensor generator is running
2. Wait 10-15 seconds for data to accumulate
3. Check backend logs for errors
4. Verify machines exist: http://localhost:8000/api/machines/

---

## 🛑 Stopping the System

To stop all services:

1. **Backend:** Press `Ctrl+C` in backend terminal
2. **Frontend:** Press `Ctrl+C` in frontend terminal
3. **Sensor Generator:** Press `Ctrl+C` in sensor generator terminal
4. **Monitoring Service:** Press `Ctrl+C` in monitoring service terminal

---

## 📝 Development Workflow

### Making Changes

1. **Backend Changes:**
   - Edit files in `backend/`
   - Server auto-reloads (if using `--reload` flag)
   - Test at: http://localhost:8000/docs

2. **Frontend Changes:**
   - Edit files in `frontend/src/`
   - Browser auto-refreshes
   - Hot Module Replacement (HMR) enabled

3. **Database Changes:**
   - Modify models in `backend/models/`
   - Database tables auto-create on restart
   - For migrations, restart the backend

---

## 🚀 Production Deployment

For production:

1. **Build Frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Backend:**
   - Use production WSGI server (gunicorn)
   - Set up environment variables
   - Configure reverse proxy (nginx)

3. **Database:**
   - Set up backups
   - Configure connection pooling
   - Enable SSL connections

---

## 📚 Additional Resources

- **API Documentation:** http://localhost:8000/docs
- **README.md:** Complete project overview
- **SETUP.md:** Detailed setup instructions
- **PROJECT_SUMMARY.md:** Feature documentation

---

## ✅ Success Checklist

- [ ] PostgreSQL database created
- [ ] Backend dependencies installed
- [ ] Database initialized with sample data
- [ ] Backend server running on port 8000
- [ ] Frontend dependencies installed
- [ ] Frontend server running on port 5173
- [ ] Sensor data generator running (optional)
- [ ] Monitoring service running (optional)
- [ ] Dashboard accessible at http://localhost:5173
- [ ] API docs accessible at http://localhost:8000/docs

---

**🎉 You're all set! The Industrial Twin system is now running.**

For questions or issues, refer to the troubleshooting section or check the logs in each terminal.











