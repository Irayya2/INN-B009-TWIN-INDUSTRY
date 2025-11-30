# ⚡ QUICK START - Get Running in 2 Minutes

## Prerequisites
- ✅ PostgreSQL installed and running
- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed

---

## 🚀 Fastest Way to Start (Windows)

### Option 1: Automated Startup (Easiest)

1. **Create Database:**
   ```bash
   createdb industrial_twin
   ```

2. **Configure Database (one-time):**
   ```bash
   cd backend
   copy .env.example .env
   notepad .env
   ```
   Update `DATABASE_URL` with your PostgreSQL credentials.

3. **Initialize Database:**
   ```bash
   init_database.bat
   ```

4. **Start Everything:**
   ```bash
   start_all.bat
   ```
   This will open separate windows for backend and frontend.

5. **Open Browser:**
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/docs

---

## 🐧 Linux/macOS Quick Start

### Automated Steps:

1. **Create Database:**
   ```bash
   createdb industrial_twin
   ```

2. **Configure Database:**
   ```bash
   cd backend
   cp .env.example .env
   nano .env
   ```
   Update `DATABASE_URL`.

3. **Initialize Database:**
   ```bash
   chmod +x init_database.sh
   ./init_database.sh
   ```

4. **Start Backend (Terminal 1):**
   ```bash
   chmod +x run_backend.sh
   ./run_backend.sh
   ```

5. **Start Frontend (Terminal 2):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. **Start Sensor Generator (Terminal 3 - Optional):**
   ```bash
   chmod +x run_sensor_generator.sh
   ./run_sensor_generator.sh
   ```

---

## 📋 Manual Step-by-Step (If Scripts Don't Work)

### 1. Database Setup
```bash
createdb industrial_twin
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/macOS

# Edit .env with your database credentials
```

### 3. Initialize Database
```bash
# From project root
python scripts/init_db.py
```

### 4. Start Backend
```bash
cd backend
python main.py
```

### 5. Start Frontend (New Terminal)
```bash
cd frontend
npm install
npm run dev
```

### 6. Start Sensor Generator (New Terminal - Optional)
```bash
cd backend/sensors_simulation
python data_generator.py
```

---

## ✅ Verification

After starting, check:

1. **Backend:** http://localhost:8000
   - Should show: `{"message":"Industrial Twin API","status":"operational"}`

2. **API Docs:** http://localhost:8000/docs
   - Should show Swagger UI

3. **Frontend:** http://localhost:5173
   - Should show dashboard

4. **Health Check:** http://localhost:8000/api/health
   - Should return: `{"status":"healthy"}`

---

## 🔧 Common Issues

### Database Connection Error
- Check PostgreSQL is running
- Verify credentials in `backend/.env`
- Test: `psql -U postgres -d industrial_twin`

### Port Already in Use
- Close other apps on ports 8000/5173
- Or change ports in config files

### Module Not Found
- Activate virtual environment
- Run: `pip install -r requirements.txt`

---

## 📚 Next Steps

Once running:
1. Explore the dashboard at http://localhost:5173
2. Check Machine Health page
3. View Supply Chain risks
4. Test API endpoints at http://localhost:8000/docs

---

## 🆘 Need Help?

- **Detailed Setup:** See `FINAL_SETUP.md`
- **Complete Guide:** See `HOW_TO_RUN.md`
- **Project Review:** See `PROJECT_REVIEW.md`

---

**🎉 You're all set! The system should now be running.**










