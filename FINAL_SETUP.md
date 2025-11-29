# 🚀 Final Setup Guide - Ready to Execute

This guide will get your Industrial Twin system up and running in **5 simple steps**.

---

## ⚡ Quick Setup (5 Steps)

### Step 1: Install PostgreSQL and Create Database

```bash
# Create the database
createdb industrial_twin

# Or using psql:
psql -U postgres
CREATE DATABASE industrial_twin;
\q
```

### Step 2: Configure Database Connection

**Windows:**
```bash
cd backend
copy .env.example .env
notepad .env
```

**Linux/macOS:**
```bash
cd backend
cp .env.example .env
nano .env
```

**Edit the DATABASE_URL in `.env`:**
```env
DATABASE_URL=postgresql+asyncpg://your_username:your_password@localhost:5432/industrial_twin
```

### Step 3: Initialize Database

**Windows:**
```bash
init_database.bat
```

**Linux/macOS:**
```bash
chmod +x init_database.sh
./init_database.sh
```

**This will:**
- Create virtual environment (if needed)
- Install Python dependencies
- Create all database tables
- Load sample data (3 machines, 2 suppliers, 3 spare parts)

### Step 4: Start Backend Server

**Windows:**
```bash
run_backend.bat
```

**Linux/macOS:**
```bash
chmod +x run_backend.sh
./run_backend.sh
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Database initialized successfully
```

✅ Backend is now running! Keep this terminal open.

**Verify:** Open http://localhost:8000 in browser - should see API welcome message.

### Step 5: Start Frontend

**Open a NEW terminal window:**

```bash
cd frontend
npm install
npm run dev
```

**You should see:**
```
VITE ready in xxx ms
➜  Local:   http://localhost:5173/
```

✅ Frontend is now running!

**Open browser:** http://localhost:5173

---

## 🎯 Optional: Generate Live Sensor Data

**Open a NEW terminal window:**

**Windows:**
```bash
run_sensor_generator.bat
```

**Linux/macOS:**
```bash
chmod +x run_sensor_generator.sh
./run_sensor_generator.sh
```

This will continuously generate sensor data every 5 seconds for all machines.

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend running: http://localhost:8000
- [ ] API Docs: http://localhost:8000/docs
- [ ] Frontend: http://localhost:5173
- [ ] Dashboard shows 3 machines
- [ ] Machine Health page loads
- [ ] Sensor data appears (after generator starts)

---

## 🔧 Troubleshooting

### Database Connection Error

**Problem:** `connection refused` or `authentication failed`

**Solution:**
1. Check PostgreSQL is running:
   ```bash
   # Windows: Check Services
   services.msc
   
   # Linux/macOS:
   sudo systemctl status postgresql
   ```

2. Verify database credentials in `backend/.env`

3. Test connection:
   ```bash
   psql -U your_username -d industrial_twin
   ```

### Port Already in Use

**Problem:** Port 8000 or 5173 already in use

**Solution:**
- Close other applications using those ports
- Or change ports in configuration files

### Module Not Found

**Problem:** `ModuleNotFoundError`

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Frontend Can't Connect to Backend

**Problem:** Network errors in browser console

**Solution:**
1. Verify backend is running on port 8000
2. Check browser console for errors
3. Verify CORS settings in `backend/main.py`

---

## 📋 Manual Setup (Alternative)

If the scripts don't work, follow manual setup:

### Backend Manual Setup

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cd ..
python scripts/init_db.py
cd backend
python main.py
```

### Frontend Manual Setup

```bash
cd frontend
npm install
npm run dev
```

### Sensor Generator Manual Setup

```bash
cd backend/sensors_simulation
# Make sure venv is activated
python data_generator.py
```

---

## 🌐 Access Points

Once everything is running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend Dashboard** | http://localhost:5173 | Main application |
| **Backend API** | http://localhost:8000 | API root |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs |
| **Health Check** | http://localhost:8000/api/health | API status |

---

## 📝 Next Steps

1. **Explore Dashboard:** View machines, alerts, and charts
2. **Check Machine Health:** See real-time sensor data
3. **View Supply Chain:** Check inventory and risks
4. **Test API:** Use Swagger UI at `/docs`
5. **Generate Data:** Start sensor generator for live data

---

## 🛑 Stopping the System

Press `Ctrl+C` in each terminal window to stop:
1. Backend server
2. Frontend server  
3. Sensor generator (if running)

---

## ✅ System Status

**All components ready:**
- ✅ Database models created
- ✅ API endpoints functional
- ✅ Frontend pages complete
- ✅ ML services implemented
- ✅ Sensor simulation ready
- ✅ Sample data loaded

**You're ready to go! 🎉**

---

For detailed documentation, see:
- `HOW_TO_RUN.md` - Detailed run instructions
- `PROJECT_REVIEW.md` - Code review
- `README.md` - Project overview








