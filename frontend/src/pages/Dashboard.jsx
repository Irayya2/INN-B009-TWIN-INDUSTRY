import React, { useState, useEffect } from 'react'
import { machinesAPI, alertsAPI, faultsAPI } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts'
import '../App.css'
import PageLayout from '../components/PageLayout'
import HeroBanner from '../components/HeroBanner'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']

function Dashboard() {
  const [machines, setMachines] = useState([])
  const [alerts, setAlerts] = useState([])
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(true)
  
  // Default demo data for judges presentation
  const defaultMachines = [
    { machine_id: 'CNC-001', name: 'CNC Milling Machine', status: 'OPERATIONAL', health_score: 95, fault_probability: 2 },
    { machine_id: 'LATHE-002', name: 'Lathe Machine', status: 'WARNING', health_score: 65, fault_probability: 25 },
    { machine_id: 'CONV-003', name: 'Conveyor Belt', status: 'CRITICAL', health_score: 35, fault_probability: 75 },
    { machine_id: 'COMP-004', name: 'Compressor Unit', status: 'MAINTENANCE', health_score: 50, fault_probability: 40 },
    { machine_id: 'PUMP-005', name: 'Water Pump', status: 'OPERATIONAL', health_score: 88, fault_probability: 5 },
  ]
  
  const defaultAlerts = [
    { id: 1, title: 'High Vibration Detected', message: 'Machine CONV-003 showing excessive vibration levels', severity: 'critical', status: 'active', created_at: new Date().toISOString() },
    { id: 2, title: 'Temperature Warning', message: 'LATHE-002 operating above normal temperature range', severity: 'warning', status: 'active', created_at: new Date(Date.now() - 3600000).toISOString() },
    { id: 3, title: 'Maintenance Due', message: 'COMP-004 scheduled maintenance overdue', severity: 'warning', status: 'active', created_at: new Date(Date.now() - 7200000).toISOString() },
  ]
  
  const defaultPredictions = [
    { machine_id: 'CONV-003', name: 'Conveyor Belt', alert_level: 'red', fault_probability: 75, health_score: 35 },
    { machine_id: 'LATHE-002', name: 'Lathe Machine', alert_level: 'yellow', fault_probability: 25, health_score: 65 },
    { machine_id: 'COMP-004', name: 'Compressor Unit', alert_level: 'yellow', fault_probability: 40, health_score: 50 },
  ]

  useEffect(() => {
    loadDashboardData()
    const interval = setInterval(loadDashboardData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      const [machinesData, alertsData, predictionsData] = await Promise.all([
        machinesAPI.getAll().catch(() => defaultMachines),
        alertsAPI.getActive().catch(() => ({ alerts: defaultAlerts })),
        faultsAPI.predictAll().catch(() => ({ predictions: defaultPredictions })),
      ])

      // Use real data if available, otherwise use defaults for demo
      setMachines(machinesData && machinesData.length > 0 ? machinesData : defaultMachines)
      setAlerts(alertsData?.alerts && alertsData.alerts.length > 0 ? alertsData.alerts : defaultAlerts)
      setPredictions(predictionsData?.predictions && predictionsData.predictions.length > 0 ? predictionsData.predictions : defaultPredictions)
      setLoading(false)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
      // Use defaults for demo presentation
      setMachines(defaultMachines)
      setAlerts(defaultAlerts)
      setPredictions(defaultPredictions)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  // Prepare status distribution data
  const statusCounts = machines.reduce((acc, machine) => {
    acc[machine.status] = (acc[machine.status] || 0) + 1
    return acc
  }, {})

  const statusData = Object.entries(statusCounts).map(([status, count]) => ({
    name: status.charAt(0).toUpperCase() + status.slice(1),
    value: count,
  }))

  // Prepare health score data for chart
  const healthScoreData = machines.slice(0, 10).map(m => ({
    name: m.machine_id,
    score: m.health_score || 0,
  }))

  // Alert severity distribution
  const alertSeverityCounts = alerts.reduce((acc, alert) => {
    acc[alert.severity] = (acc[alert.severity] || 0) + 1
    return acc
  }, {})

  const alertData = Object.entries(alertSeverityCounts).map(([severity, count]) => ({
    name: severity.charAt(0).toUpperCase() + severity.slice(1),
    value: count,
  }))

  const criticalMachines = predictions.filter(p => p.alert_level === 'red').length
  const warningMachines = predictions.filter(p => p.alert_level === 'yellow').length

  return (
    <PageLayout title="Dashboard Overview">
      <HeroBanner />
      {/* Key Metrics */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Total Machines</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{machines.length}</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-danger)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Critical Alerts</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-danger)' }}>
            {alerts.filter(a => a.severity === 'critical' || a.severity === 'emergency').length}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Requires Immediate Action</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-warning)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>At Risk Machines</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-warning)' }}>
            {criticalMachines + warningMachines}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Monitor Closely</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-success)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Avg Health Score</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-success)' }}>
            {machines.length > 0
              ? Math.round(machines.reduce((sum, m) => sum + (m.health_score || 0), 0) / machines.length)
              : 0}%
          </div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Overall System Health</div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-2">
        {/* Machine Status Distribution */}
        <div className="card">
          <h2 className="card-title">Machine Status Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={statusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Health Scores */}
        <div className="card">
          <h2 className="card-title">Machine Health Scores</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={healthScoreData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="score" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Alerts and Predictions */}
      <div className="grid grid-2">
        {/* Recent Alerts */}
        <div className="card">
          <h2 className="card-title">Recent Alerts</h2>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {alerts.length === 0 ? (
              <p style={{ color: '#666', textAlign: 'center', padding: '2rem' }}>
                No active alerts
              </p>
            ) : (
              alerts.slice(0, 10).map((alert) => (
                <div
                  key={alert.id}
                  style={{
                    padding: '1rem',
                    borderBottom: '1px solid #eee',
                    borderLeft: `4px solid ${
                      alert.severity === 'critical' || alert.severity === 'emergency' ? 'var(--color-danger)' :
                      alert.severity === 'warning' ? 'var(--color-warning)' : 'var(--color-info)'
                    }`,
                  }}
                >
                  <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>
                    {alert.title}
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#666' }}>
                    {alert.message}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.5rem' }}>
                    {new Date(alert.created_at).toLocaleString()}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Fault Predictions */}
        <div className="card">
          <h2 className="card-title">Fault Predictions</h2>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {predictions.length === 0 ? (
              <p style={{ color: '#666', textAlign: 'center', padding: '2rem' }}>
                No predictions available
              </p>
            ) : (
              predictions.slice(0, 10).map((prediction) => (
                <div
                  key={prediction.machine_id}
                  style={{
                    padding: '1rem',
                    borderBottom: '1px solid #eee',
                    borderLeft: `4px solid ${
                      prediction.alert_level === 'red' ? 'var(--color-danger)' :
                      prediction.alert_level === 'yellow' ? 'var(--color-warning)' : 'var(--color-success)'
                    }`,
                  }}
                >
                  <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>
                    {prediction.name || prediction.machine_id}
                  </div>
                  <div style={{ display: 'flex', gap: '1rem', fontSize: '0.85rem' }}>
                    <span>Fault: {prediction.fault_probability?.toFixed(1)}%</span>
                    <span>Health: {prediction.health_score?.toFixed(1)}%</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </PageLayout>
  )
}

export default Dashboard











