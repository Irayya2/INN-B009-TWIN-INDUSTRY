import React, { useState, useEffect } from 'react'
import { machinesAPI, sensorsAPI, faultsAPI } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import '../App.css'
import PageLayout from '../components/PageLayout'

function MachineHealth() {
  const [machines, setMachines] = useState([])
  const [selectedMachine, setSelectedMachine] = useState(null)
  const [sensorData, setSensorData] = useState([])
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMachines()
  }, [])

  useEffect(() => {
    if (selectedMachine) {
      loadMachineData(selectedMachine)
      const interval = setInterval(() => loadMachineData(selectedMachine), 10000)
      return () => clearInterval(interval)
    }
  }, [selectedMachine])

  const loadMachines = async () => {
    try {
      const data = await machinesAPI.getAll()
      setMachines(data || [])
      if (data && data.length > 0 && !selectedMachine) {
        setSelectedMachine(data[0].machine_id)
      }
      setLoading(false)
    } catch (error) {
      console.error('Error loading machines:', error)
      setLoading(false)
    }
  }

  const loadMachineData = async (machineId) => {
    try {
      const [sensorDataRes, predictionRes] = await Promise.all([
        sensorsAPI.getTimeframe(machineId, 24),
        faultsAPI.predict(machineId).catch(() => null),
      ])

      setSensorData(sensorDataRes || [])
      setPrediction(predictionRes || null)
    } catch (error) {
      console.error('Error loading machine data:', error)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  const machine = machines.find(m => m.machine_id === selectedMachine)

  // Prepare chart data
  const chartData = sensorData.slice(-50).map(sd => ({
    time: new Date(sd.timestamp).toLocaleTimeString(),
    vibration: sd.vibration,
    temperature: sd.temperature,
    rpm: sd.rpm,
    load: sd.load,
    acoustic: sd.acoustic_noise,
  }))

  const getHealthColor = (score) => {
    if (score >= 80) return '#28a745'
    if (score >= 60) return '#ffc107'
    return '#dc3545'
  }

  const getAlertLevelColor = (level) => {
    if (level === 'green') return '#28a745'
    if (level === 'yellow') return '#ffc107'
    return '#dc3545'
  }

  return (
    <PageLayout title="Machine Health Monitoring">
      {/* Machine Selector */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <label style={{ fontWeight: '600', marginRight: '1rem' }}>Select Machine:</label>
        <select
          value={selectedMachine || ''}
          onChange={(e) => setSelectedMachine(e.target.value)}
          style={{
            padding: '0.5rem 1rem',
            borderRadius: '6px',
            border: '1px solid #ddd',
            fontSize: '1rem',
            minWidth: '200px',
          }}
        >
          {machines.map(m => (
            <option key={m.machine_id} value={m.machine_id}>
              {m.name} ({m.machine_id})
            </option>
          ))}
        </select>
      </div>

      {machine && (
        <>
          {/* Machine Status Cards */}
          <div className="grid grid-4" style={{ marginBottom: '1.5rem' }}>
            <div className="card">
              <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Health Score</h3>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: getHealthColor(machine.health_score || 0) }}>
                {(machine.health_score || 0).toFixed(1)}%
              </div>
            </div>
            <div className="card">
              <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Fault Probability</h3>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#dc3545' }}>
                {(machine.fault_probability || 0).toFixed(1)}%
              </div>
            </div>
            <div className="card">
              <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Status</h3>
              </div>
            </PageLayout>
          )
                </span>
              </div>
            </div>
            <div className="card">
              <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Alert Level</h3>
              <div>
                {prediction && (
                  <span style={{
                    fontSize: '1.2rem',
                    fontWeight: 'bold',
                    color: getAlertLevelColor(prediction.alert_level),
                  }}>
                    {prediction.alert_level.toUpperCase()}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Prediction Details */}
          {prediction && (
            <div className="card" style={{ marginBottom: '1.5rem' }}>
              <h2 className="card-title">Fault Prediction Details</h2>
              <div className="grid grid-2">
                <div>
                  <p><strong>Anomaly Score:</strong> {prediction.anomaly_score?.toFixed(2)}%</p>
                  <p><strong>Predicted Failure Window:</strong> {prediction.predicted_failure_window || 'N/A'}</p>
                  {prediction.risk_factors && prediction.risk_factors.length > 0 && (
                    <div>
                      <strong>Risk Factors:</strong>
                      <ul style={{ marginTop: '0.5rem', paddingLeft: '1.5rem' }}>
                        {prediction.risk_factors.map((factor, idx) => (
                          <li key={idx}>{factor}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
                <div>
                  {prediction.recommendations && prediction.recommendations.length > 0 && (
                    <div>
                      <strong>Recommendations:</strong>
                      <ul style={{ marginTop: '0.5rem', paddingLeft: '1.5rem' }}>
                        {prediction.recommendations.map((rec, idx) => (
                          <li key={idx}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Sensor Data Charts */}
          <div className="grid grid-2">
            <div className="card">
              <h2 className="card-title">Vibration & Temperature (Last 50 readings)</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Line yAxisId="left" type="monotone" dataKey="vibration" stroke="#8884d8" name="Vibration (mm/s)" />
                  <Line yAxisId="right" type="monotone" dataKey="temperature" stroke="#82ca9d" name="Temperature (°C)" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="card">
              <h2 className="card-title">RPM & Load (Last 50 readings)</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="rpm" stroke="#ffc658" name="RPM" />
                  <Line type="monotone" dataKey="load" stroke="#ff7300" name="Load (%)" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Latest Sensor Reading */}
          {sensorData.length > 0 && (
            <div className="card" style={{ marginTop: '1.5rem' }}>
              <h2 className="card-title">Latest Sensor Reading</h2>
              <div className="grid grid-4">
                <div>
                  <strong>Vibration:</strong> {sensorData[sensorData.length - 1]?.vibration?.toFixed(2)} mm/s
                </div>
                <div>
                  <strong>Temperature:</strong> {sensorData[sensorData.length - 1]?.temperature?.toFixed(2)} °C
                </div>
                <div>
                  <strong>Acoustic Noise:</strong> {sensorData[sensorData.length - 1]?.acoustic_noise?.toFixed(2)} dB
                </div>
                <div>
                  <strong>Load:</strong> {sensorData[sensorData.length - 1]?.load?.toFixed(2)} %
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default MachineHealth









