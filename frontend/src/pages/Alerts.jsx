import React, { useState, useEffect } from 'react'
import { alertsAPI } from '../services/api'
import '../App.css'
import PageLayout from '../components/PageLayout'

const defaultAlerts = []


function Alerts() {
  const [alerts, setAlerts] = useState([])
  const [filter, setFilter] = useState({ status: 'active', severity: '' })
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(new Set())
  const [message, setMessage] = useState({ type: '', text: '' })

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
      // Use real data if available, otherwise use defaults for demo
      setAlerts(data && data.length > 0 ? data : defaultAlerts)
      setLoading(false)
    } catch (error) {
      console.error('Error loading alerts:', error)
      // Use defaults for demo presentation
      setAlerts(defaultAlerts)
      setLoading(false)
    }
  }

  const handleAcknowledge = async (alertId) => {
    setProcessing(prev => new Set(prev).add(`ack-${alertId}`))
    try {
      await alertsAPI.acknowledge(alertId, 'System User')
      setMessage({ type: 'success', text: 'Alert acknowledged successfully' })
      loadAlerts()
      setTimeout(() => setMessage({ type: '', text: '' }), 3000)
    } catch (error) {
      console.error('Error acknowledging alert:', error)
      setMessage({ type: 'error', text: 'Failed to acknowledge alert' })
      setTimeout(() => setMessage({ type: '', text: '' }), 3000)
    } finally {
      setProcessing(prev => {
        const next = new Set(prev)
        next.delete(`ack-${alertId}`)
        return next
      })
    }
  }

  const handleResolve = async (alertId) => {
    setProcessing(prev => new Set(prev).add(`resolve-${alertId}`))
    try {
      await alertsAPI.resolve(alertId)
      setMessage({ type: 'success', text: 'Alert resolved successfully' })
      loadAlerts()
      setTimeout(() => setMessage({ type: '', text: '' }), 3000)
    } catch (error) {
      console.error('Error resolving alert:', error)
      setMessage({ type: 'error', text: 'Failed to resolve alert' })
      setTimeout(() => setMessage({ type: '', text: '' }), 3000)
    } finally {
      setProcessing(prev => {
        const next = new Set(prev)
        next.delete(`resolve-${alertId}`)
        return next
      })
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
      case 'emergency':
      case 'danger':
        return 'var(--color-danger)'  // Red
      case 'warning':
      case 'caution':
        return 'var(--color-warning)'  // Yellow
      case 'info':
      case 'safe':
        return 'var(--color-info)'  // Blue
      default:
        return 'var(--color-success)'  // Green - Normal
    }
  }

  const getSeverityBgColor = (severity) => {
    switch (severity) {
      case 'critical':
      case 'emergency':
      case 'danger':
        return 'var(--bg-danger)'
      case 'warning':
      case 'caution':
        return 'var(--bg-warning)'
      case 'info':
      case 'safe':
        return 'var(--bg-info)'
      default:
        return 'var(--bg-success)'
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
            animation: 'slideIn 0.3s ease-out'
          }}
        >
          {message.text}
        </div>
      )}
      {/* Summary Cards */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Total Alerts</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{alerts.length}</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-danger)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Critical</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-danger)' }}>{criticalAlerts}</div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Immediate Action Required</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-warning)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Warnings</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-warning)' }}>{warningAlerts}</div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Monitor & Review</div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid var(--color-info)' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Active</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-info)' }}>
            {alerts.filter(a => a.status === 'active').length}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.25rem' }}>Currently Active</div>
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
                  backgroundColor: alert.status === 'active' ? getSeverityBgColor(alert.severity) + '40' : 'transparent',
                  boxShadow: alert.status === 'active' ? `0 2px 8px ${getSeverityColor(alert.severity)}20` : 'none',
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
                          disabled={processing.has(`ack-${alert.id}`) || processing.has(`resolve-${alert.id}`)}
                          style={{ 
                            fontSize: '0.85rem',
                            opacity: processing.has(`ack-${alert.id}`) ? 0.6 : 1,
                            cursor: processing.has(`ack-${alert.id}`) ? 'not-allowed' : 'pointer'
                          }}
                        >
                          {processing.has(`ack-${alert.id}`) ? 'Processing...' : 'Acknowledge'}
                        </button>
                        <button
                          className="btn btn-primary"
                          onClick={() => handleResolve(alert.id)}
                          disabled={processing.has(`ack-${alert.id}`) || processing.has(`resolve-${alert.id}`)}
                          style={{ 
                            fontSize: '0.85rem',
                            opacity: processing.has(`resolve-${alert.id}`) ? 0.6 : 1,
                            cursor: processing.has(`resolve-${alert.id}`) ? 'not-allowed' : 'pointer'
                          }}
                        >
                          {processing.has(`resolve-${alert.id}`) ? 'Processing...' : 'Resolve'}
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











