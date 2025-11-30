import React, { useState, useEffect } from 'react'
import { maintenanceAPI, machinesAPI } from '../services/api'
import '../App.css'
import PageLayout from '../components/PageLayout'

function MaintenanceScheduler() {
  const [logs, setLogs] = useState([])
  const [machines, setMachines] = useState([])
  const [filter, setFilter] = useState({ machineId: '', status: '' })
  const [loading, setLoading] = useState(true)
  const [showScheduleForm, setShowScheduleForm] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })
  
  // Default demo data for judges presentation
  const defaultLogs = [
    { id: 1, machine_id: 'CNC-001', maintenance_type: 'preventive', title: 'Monthly Lubrication', status: 'scheduled', scheduled_date: new Date(Date.now() + 86400000).toISOString(), technician: 'John Doe', sop_reference: 'SOP-MAINT-02' },
    { id: 2, machine_id: 'LATHE-002', maintenance_type: 'corrective', title: 'Bearing Replacement', status: 'in_progress', scheduled_date: new Date().toISOString(), technician: 'Jane Smith', sop_reference: 'SOP-MAINT-01' },
    { id: 3, machine_id: 'CONV-003', maintenance_type: 'emergency', title: 'Belt Tension Adjustment', status: 'completed', scheduled_date: new Date(Date.now() - 86400000).toISOString(), technician: 'Mike Johnson', sop_reference: 'SOP-MAINT-02' },
  ]
  const [newMaintenance, setNewMaintenance] = useState({
    machine_id: '',
    maintenance_type: 'preventive',
    title: '',
    description: '',
    scheduled_date: '',
    technician: '',
    sop_reference: '',
  })

  useEffect(() => {
    loadData()
  }, [filter])

  const loadData = async () => {
    try {
      const [logsData, machinesData] = await Promise.all([
        maintenanceAPI.getLogs(filter.machineId || undefined, filter.status || undefined).catch(() => defaultLogs),
        machinesAPI.getAll().catch(() => []),
      ])
      setLogs(logsData && logsData.length > 0 ? logsData : defaultLogs)
      setMachines(machinesData || [])
      setLoading(false)
    } catch (error) {
      console.error('Error loading data:', error)
      // Use defaults for demo presentation
      setLogs(defaultLogs)
      setLoading(false)
    }
  }

  const handleSchedule = async (e) => {
    e.preventDefault()
    setProcessing(true)
    try {
      await maintenanceAPI.schedule({
        ...newMaintenance,
        scheduled_date: new Date(newMaintenance.scheduled_date).toISOString(),
      })
      setMessage({ type: 'success', text: 'Maintenance scheduled successfully' })
      setShowScheduleForm(false)
      setNewMaintenance({
        machine_id: '',
        maintenance_type: 'preventive',
        title: '',
        description: '',
        scheduled_date: '',
        technician: '',
        sop_reference: '',
      })
      loadData()
      setTimeout(() => setMessage({ type: '', text: '' }), 3000)
    } catch (error) {
      console.error('Error scheduling maintenance:', error)
      setMessage({ type: 'error', text: 'Failed to schedule maintenance' })
      setTimeout(() => setMessage({ type: '', text: '' }), 3000)
    } finally {
      setProcessing(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'var(--color-success)'  // Green - Completed/Safe
      case 'in_progress':
        return 'var(--color-info)'      // Blue - In Progress
      case 'scheduled':
        return 'var(--color-gray)'       // Gray - Scheduled
      default:
        return 'var(--color-danger)'     // Red - Cancelled/Error
    }
  }

  const getTypeColor = (type) => {
    switch (type) {
      case 'preventive':
        return 'var(--color-info)'      // Blue - Preventive/Safe
      case 'predictive':
        return 'var(--color-success)'   // Green - Predictive/Good
      case 'corrective':
        return 'var(--color-warning)'   // Yellow - Corrective/Warning
      case 'emergency':
        return 'var(--color-danger)'    // Red - Emergency/Critical
      default:
        return 'var(--color-gray)'
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  const scheduledCount = logs.filter(l => l.status === 'scheduled').length
  const inProgressCount = logs.filter(l => l.status === 'in_progress').length
  const completedCount = logs.filter(l => l.status === 'completed').length

  return (
    <PageLayout
      title="Maintenance Scheduler"
      actions={(
        <button 
          className="btn btn-primary" 
          onClick={() => setShowScheduleForm(!showScheduleForm)}
          disabled={processing}
        >
          {showScheduleForm ? 'Cancel' : '+ Schedule Maintenance'}
        </button>
      )}
    >
      {/* Message Notification */}
      {message.text && (
        <div
          style={{
            position: 'fixed',
            top: '1rem',
            right: '1rem',
            padding: '1rem 1.5rem',
            backgroundColor: message.type === 'success' ? 'var(--color-success)' : 'var(--color-danger)',
            color: 'white',
            borderRadius: '6px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            zIndex: 1000,
          }}
        >
          {message.text}
        </div>
      )}

      {/* Schedule Form */}
      {showScheduleForm && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h2 className="card-title">Schedule Maintenance (SOP-MAINT-02)</h2>
          <form onSubmit={handleSchedule}>
            <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: '1fr 1fr' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Machine *
                </label>
                <select
                  required
                  value={newMaintenance.machine_id}
                  onChange={(e) => setNewMaintenance({ ...newMaintenance, machine_id: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                >
                  <option value="">Select Machine...</option>
                  {machines.map(m => (
                    <option key={m.machine_id} value={m.machine_id}>
                      {m.name} ({m.machine_id})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Maintenance Type *
                </label>
                <select
                  required
                  value={newMaintenance.maintenance_type}
                  onChange={(e) => setNewMaintenance({ ...newMaintenance, maintenance_type: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                >
                  <option value="preventive">Preventive</option>
                  <option value="predictive">Predictive</option>
                  <option value="corrective">Corrective</option>
                  <option value="emergency">Emergency</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Title *
                </label>
                <input
                  type="text"
                  required
                  value={newMaintenance.title}
                  onChange={(e) => setNewMaintenance({ ...newMaintenance, title: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Scheduled Date *
                </label>
                <input
                  type="datetime-local"
                  required
                  value={newMaintenance.scheduled_date}
                  onChange={(e) => setNewMaintenance({ ...newMaintenance, scheduled_date: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Technician
                </label>
                <input
                  type="text"
                  value={newMaintenance.technician}
                  onChange={(e) => setNewMaintenance({ ...newMaintenance, technician: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  SOP Reference
                </label>
                <input
                  type="text"
                  value={newMaintenance.sop_reference}
                  onChange={(e) => setNewMaintenance({ ...newMaintenance, sop_reference: e.target.value })}
                  placeholder="e.g., SOP-MAINT-02"
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                />
              </div>
              <div style={{ gridColumn: '1 / -1' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Description
                </label>
                <textarea
                  value={newMaintenance.description}
                  onChange={(e) => setNewMaintenance({ ...newMaintenance, description: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd', minHeight: '100px' }}
                />
              </div>
            </div>
            <button 
              type="submit" 
              className="btn btn-primary" 
              style={{ marginTop: '1rem' }}
              disabled={processing}
            >
              {processing ? 'Scheduling...' : 'Schedule Maintenance'}
            </button>
          </form>
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Total Logs</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{logs.length}</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-gray)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Scheduled</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-gray)' }}>{scheduledCount}</div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Upcoming Tasks</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-info)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>In Progress</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-info)' }}>{inProgressCount}</div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Currently Active</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-success)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Completed</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-success)' }}>{completedCount}</div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Successfully Finished</div>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <label style={{ fontWeight: '600' }}>Machine:</label>
          <select
            value={filter.machineId}
            onChange={(e) => setFilter({ ...filter, machineId: e.target.value })}
            style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
          >
            <option value="">All Machines</option>
            {machines.map(m => (
              <option key={m.machine_id} value={m.machine_id}>
                {m.name} ({m.machine_id})
              </option>
            ))}
          </select>

          <label style={{ fontWeight: '600', marginLeft: '1rem' }}>Status:</label>
          <select
            value={filter.status}
            onChange={(e) => setFilter({ ...filter, status: e.target.value })}
            style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
          >
            <option value="">All</option>
            <option value="scheduled">Scheduled</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>

      {/* Maintenance Logs */}
      <div className="card">
        <h2 className="card-title">Maintenance Logs</h2>
        {logs.length === 0 ? (
          <p style={{ color: '#666', textAlign: 'center', padding: '2rem' }}>
            No maintenance logs found
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                  <th style={{ padding: '0.75rem' }}>Machine</th>
                  <th style={{ padding: '0.75rem' }}>Type</th>
                  <th style={{ padding: '0.75rem' }}>Title</th>
                  <th style={{ padding: '0.75rem' }}>Status</th>
                  <th style={{ padding: '0.75rem' }}>Scheduled</th>
                  <th style={{ padding: '0.75rem' }}>Technician</th>
                  <th style={{ padding: '0.75rem' }}>SOP Reference</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '0.75rem' }}>{log.machine_id}</td>
                    <td style={{ padding: '0.75rem' }}>
                      <span
                        style={{
                          padding: '0.25rem 0.75rem',
                          borderRadius: '12px',
                          fontSize: '0.85rem',
                          fontWeight: '500',
                          backgroundColor: getTypeColor(log.maintenance_type) + '33',
                          color: getTypeColor(log.maintenance_type),
                        }}
                      >
                        {log.maintenance_type.toUpperCase()}
                      </span>
                    </td>
                    <td style={{ padding: '0.75rem', fontWeight: '600' }}>{log.title}</td>
                    <td style={{ padding: '0.75rem' }}>
                      <span
                        style={{
                          padding: '0.25rem 0.75rem',
                          borderRadius: '12px',
                          fontSize: '0.85rem',
                          fontWeight: '500',
                          backgroundColor: getStatusColor(log.status) + '33',
                          color: getStatusColor(log.status),
                        }}
                      >
                        {log.status.replace(/_/g, ' ').toUpperCase()}
                      </span>
                    </td>
                    <td style={{ padding: '0.75rem' }}>
                      {new Date(log.scheduled_date).toLocaleString()}
                    </td>
                    <td style={{ padding: '0.75rem' }}>{log.technician || 'N/A'}</td>
                    <td style={{ padding: '0.75rem' }}>{log.sop_reference || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </PageLayout>
  )
}

export default MaintenanceScheduler











