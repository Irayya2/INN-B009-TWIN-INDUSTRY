# Setup Guide

## Prerequisites

1. **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download Node.js](https://nodejs.org/)
3. **PostgreSQL 14+** - [Download PostgreSQL](https://www.postgresql.org/download/)
4. **Git** (optional) - For version control

## Step 1: Database Setup

1. **Install PostgreSQL** and ensure it's running

2. **Create the database:**
```bash
createdb industrial_twin
```

3. **Configure database connection:**
   - Copy `backend/.env.example` to `backend/.env`
   - Update the `DATABASE_URL` in `backend/.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://your_username:your_password@localhost:5432/industrial_twin
   ```

## Step 2: Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize the database and create sample data:**
```bash
# From the project root directory
cd ..
python scripts/init_db.py
```

5. **Start the FastAPI server:**
```bash
cd backend
python main.py
# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

## Step 3: Frontend Setup

1. **Navigate to frontend directory (in a new terminal):**
```bash
cd frontend
```

2. **Install Node.js dependencies:**
```bash
npm install
# or
yarn install
```

3. **Start the development server:**
```bash
npm run dev
# or
yarn dev
```

The frontend will be available at: http://localhost:5173

## Step 4: Start Sensor Data Generator (Optional)

In a separate terminal, start the sensor data simulator to generate real-time data:

```bash
cd backend/sensors_simulation
python data_generator.py
```

This will continuously generate and push sensor data to the API every 5 seconds.

## Step 5: Start Monitoring Service (Optional)

In another terminal, start the monitoring service:

```bash
cd backend/monitoring
python monitoring_service.py
```

This service continuously monitors machines, runs predictions, and generates alerts.

## Verification

1. **Check API health:**
   - Open: http://localhost:8000/api/health
   - Should return: `{"status": "healthy", "service": "industrial-twin-api"}`

2. **Check frontend:**
   - Open: http://localhost:5173
   - You should see the Industrial Twin dashboard

3. **Check API documentation:**
   - Open: http://localhost:8000/docs
   - Interactive API documentation with Swagger UI

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `pg_isready`
- Check database credentials in `backend/.env`
- Verify the database exists: `psql -l | grep industrial_twin`

### Port Already in Use
- Backend (port 8000): Change port in `backend/main.py` or use `--port` flag
- Frontend (port 5173): Change port in `frontend/vite.config.js`

### Missing Dependencies
- Backend: Re-run `pip install -r requirements.txt`
- Frontend: Delete `node_modules` and re-run `npm install`

### Import Errors
- Ensure you're in the correct directory
- Check Python path and virtual environment activation
- Verify all `__init__.py` files exist in package directories

## Production Deployment

For production deployment:

1. **Backend:**
   - Use a production WSGI server (gunicorn with uvicorn workers)
   - Set up proper environment variables
   - Configure database connection pooling
   - Enable logging and monitoring

2. **Frontend:**
   - Build production bundle: `npm run build`
   - Serve static files with a web server (nginx, Apache)
   - Configure API proxy for backend

3. **Database:**
   - Set up database backups
   - Configure connection pooling
   - Enable query logging for performance monitoring

## Next Steps

1. Explore the dashboard at http://localhost:5173
2. Check machine health in the Machine Health page
3. Review supply chain risks in the Supply Chain page
4. Monitor alerts in real-time
5. Create SOP tasks and schedule maintenance

## Support

For issues or questions, refer to the main README.md or contact the development team.











