import React, { useState, useEffect } from 'react'
import { alertsAPI } from '../services/api'
import '../App.css'
import PageLayout from '../components/PageLayout'

function Alerts() {
  const [alerts, setAlerts] = useState([])
  const [filter, setFilter] = useState({ status: 'active', severity: '' })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAlerts()
    const interval = setInterval(loadAlerts, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [filter])

  const loadAlerts = async () => {
    try {
      let data
      if (filter.status === 'active') {
        const response = await alertsAPI.getActive()
        data = response.alerts || []
      } else {
        data = await alertsAPI.getAll(filter.status, filter.severity)
      }
      setAlerts(data)
      setLoading(false)
    } catch (error) {
      console.error('Error loading alerts:', error)
      setLoading(false)
    }
  }

  const handleAcknowledge = async (alertId) => {
    try {
      await alertsAPI.acknowledge(alertId, 'System User')
      loadAlerts()
    } catch (error) {
      console.error('Error acknowledging alert:', error)
      alert('Failed to acknowledge alert')
    }
  }

  const handleResolve = async (alertId) => {
    try {
      await alertsAPI.resolve(alertId)
      loadAlerts()
    } catch (error) {
      console.error('Error resolving alert:', error)
      alert('Failed to resolve alert')
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
      case 'emergency':
        return '#dc3545'
      case 'warning':
        return '#ffc107'
      default:
        return '#17a2b8'
    }
  }

  const getSeverityBgColor = (severity) => {
    switch (severity) {
      case 'critical':
      case 'emergency':
        return '#f8d7da'
      case 'warning':
        return '#fff3cd'
      default:
        return '#d1ecf1'
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  const criticalAlerts = alerts.filter(a => a.severity === 'critical' || a.severity === 'emergency').length
  const warningAlerts = alerts.filter(a => a.severity === 'warning').length

  return (
    <PageLayout title="System Alerts">
      {/* Summary Cards */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Total Alerts</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{alerts.length}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Critical</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#dc3545' }}>{criticalAlerts}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Warnings</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#ffc107' }}>{warningAlerts}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Active</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#17a2b8' }}>
            {alerts.filter(a => a.status === 'active').length}
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <label style={{ fontWeight: '600' }}>Status:</label>
          <select
            value={filter.status}
            onChange={(e) => setFilter({ ...filter, status: e.target.value })}
            style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
          >
            <option value="active">Active</option>
            <option value="acknowledged">Acknowledged</option>
            <option value="resolved">Resolved</option>
            <option value="">All</option>
          </select>

          <label style={{ fontWeight: '600', marginLeft: '1rem' }}>Severity:</label>
          <select
            value={filter.severity}
            onChange={(e) => setFilter({ ...filter, severity: e.target.value })}
            style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
          >
            <option value="">All</option>
            <option value="critical">Critical</option>
            <option value="warning">Warning</option>
            <option value="info">Info</option>
          </select>
        </div>
      </div>

      {/* Alerts List */}
      <div className="card">
        <h2 className="card-title">Alerts</h2>
        {alerts.length === 0 ? (
          <p style={{ color: '#666', textAlign: 'center', padding: '2rem' }}>
            No alerts found
          </p>
        ) : (
          <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
            {alerts.map((alert) => (
              <div
                key={alert.id}
                style={{
                  padding: '1.5rem',
                  borderBottom: '1px solid #eee',
                  borderLeft: `4px solid ${getSeverityColor(alert.severity)}`,
                  backgroundColor: alert.status === 'active' ? getSeverityBgColor(alert.severity) + '33' : 'transparent',
                  marginBottom: '0.5rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                  <div>
                    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <span
                        style={{
                          padding: '0.25rem 0.75rem',
                          borderRadius: '12px',
                          fontSize: '0.85rem',
                          fontWeight: '600',
                          backgroundColor: getSeverityColor(alert.severity),
                          color: 'white',
                        }}
                      >
                        {alert.severity.toUpperCase()}
                      </span>
                      <span
                        style={{
                          padding: '0.25rem 0.75rem',
                          borderRadius: '12px',
                          fontSize: '0.85rem',
                          backgroundColor: '#e9ecef',
                          color: '#495057',
                        }}
                      >
                        {alert.alert_type.replace(/_/g, ' ').toUpperCase()}
                      </span>
                      <span className={`status-badge status-${alert.status}`}>
                        {alert.status}
                      </span>
                    </div>
                    <h3 style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                      {alert.title}
                    </h3>
                    <p style={{ color: '#666', marginBottom: '0.5rem' }}>{alert.message}</p>
                  </div>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    {alert.status === 'active' && (
                      <>
                        <button
                          className="btn btn-secondary"
                          onClick={() => handleAcknowledge(alert.id)}
                          style={{ fontSize: '0.85rem' }}
                        >
                          Acknowledge
                        </button>
                        <button
                          className="btn btn-primary"
                          onClick={() => handleResolve(alert.id)}
                          style={{ fontSize: '0.85rem' }}
                        >
                          Resolve
                        </button>
                      </>
                    )}
                  </div>
                </div>

                {alert.fault_probability !== null && alert.fault_probability !== undefined && (
                  <div style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem' }}>
                    <strong>Fault Probability:</strong> {alert.fault_probability.toFixed(1)}%
                  </div>
                )}

                {alert.predicted_failure_window && (
                  <div style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.25rem' }}>
                    <strong>Predicted Failure Window:</strong> {alert.predicted_failure_window}
                  </div>
                )}

                <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.75rem' }}>
                  Created: {new Date(alert.created_at).toLocaleString()}
                  {alert.acknowledged_at && ` | Acknowledged: ${new Date(alert.acknowledged_at).toLocaleString()}`}
                  {alert.resolved_at && ` | Resolved: ${new Date(alert.resolved_at).toLocaleString()}`}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </PageLayout>
  )
}

export default Alerts









