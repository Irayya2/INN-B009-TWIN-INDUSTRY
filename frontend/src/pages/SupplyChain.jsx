import React, { useState, useEffect } from 'react'
import { supplyChainAPI } from '../services/api'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import '../App.css'
import PageLayout from '../components/PageLayout'

const RISK_COLORS = {
  low: '#28a745',
  medium: '#ffc107',
  high: '#ff9800',
  critical: '#dc3545',
}

function SupplyChain() {
  const [risks, setRisks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSupplyChainRisks()
    const interval = setInterval(loadSupplyChainRisks, 60000) // Refresh every minute
    return () => clearInterval(interval)
  }, [])

  const loadSupplyChainRisks = async () => {
    try {
      const data = await supplyChainAPI.getAllRisks()
      setRisks(data.risks || [])
      setLoading(false)
    } catch (error) {
      console.error('Error loading supply chain risks:', error)
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

  // Prepare risk distribution data
  const riskDistribution = risks.reduce((acc, risk) => {
    acc[risk.risk_level] = (acc[risk.risk_level] || 0) + 1
    return acc
  }, {})

  const riskChartData = Object.entries(riskDistribution).map(([level, count]) => ({
    name: level.charAt(0).toUpperCase() + level.slice(1),
    value: count,
  }))

  // Top risks
  const topRisks = [...risks]
    .sort((a, b) => b.risk_score - a.risk_score)
    .slice(0, 10)

  const riskBarData = topRisks.map(risk => ({
    name: risk.part_name || risk.part_number,
    score: risk.risk_score,
    level: risk.risk_level,
  }))

  const criticalRisks = risks.filter(r => r.risk_level === 'critical').length
  const highRisks = risks.filter(r => r.risk_level === 'high').length

  return (
    <PageLayout title="Supply Chain Risk Management">
      {/* Key Metrics */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Total Parts Monitored</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{risks.length}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Critical Risks</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#dc3545' }}>{criticalRisks}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>High Risks</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#ff9800' }}>{highRisks}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Avg Risk Score</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>
            {risks.length > 0
              ? Math.round(risks.reduce((sum, r) => sum + (r.risk_score || 0), 0) / risks.length)
              : 0}
          </div>
        </div>
      </PageLayout>
    )
      {/* Charts */}
      <div className="grid grid-2">
        <div className="card">
          <h2 className="card-title">Risk Level Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskChartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {riskChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={RISK_COLORS[entry.name.toLowerCase()] || '#8884d8'} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2 className="card-title">Top 10 Risk Scores</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={riskBarData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="score" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Risk Details Table */}
      <div className="card">
        <h2 className="card-title">Supply Chain Risk Details</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                <th style={{ padding: '0.75rem' }}>Part Number</th>
                <th style={{ padding: '0.75rem' }}>Part Name</th>
                <th style={{ padding: '0.75rem' }}>Current Stock</th>
                <th style={{ padding: '0.75rem' }}>Risk Level</th>
                <th style={{ padding: '0.75rem' }}>Risk Score</th>
                <th style={{ padding: '0.75rem' }}>Predicted Delay</th>
                <th style={{ padding: '0.75rem' }}>Stockout Prob.</th>
                <th style={{ padding: '0.75rem' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {risks.length === 0 ? (
                <tr>
                  <td colSpan="8" style={{ padding: '2rem', textAlign: 'center', color: '#666' }}>
                    No supply chain risks found
                  </td>
                </tr>
              ) : (
                risks
                  .sort((a, b) => b.risk_score - a.risk_score)
                  .map((risk) => (
                    <tr key={risk.part_id} style={{ borderBottom: '1px solid #eee' }}>
                      <td style={{ padding: '0.75rem' }}>{risk.part_number}</td>
                      <td style={{ padding: '0.75rem' }}>{risk.part_name}</td>
                      <td style={{ padding: '0.75rem' }}>
                        {risk.current_quantity} / {risk.min_quantity || 'N/A'}
                      </td>
                      <td style={{ padding: '0.75rem' }}>
                        <span
                          style={{
                            padding: '0.25rem 0.75rem',
                            borderRadius: '12px',
                            fontSize: '0.85rem',
                            fontWeight: '500',
                            backgroundColor: RISK_COLORS[risk.risk_level] + '33',
                            color: RISK_COLORS[risk.risk_level],
                          }}
                        >
                          {risk.risk_level.toUpperCase()}
                        </span>
                      </td>
                      <td style={{ padding: '0.75rem', fontWeight: '600' }}>
                        {risk.risk_score?.toFixed(1)}%
                      </td>
                      <td style={{ padding: '0.75rem' }}>
                        {risk.predicted_delay_days ? `${risk.predicted_delay_days.toFixed(1)} days` : 'N/A'}
                      </td>
                      <td style={{ padding: '0.75rem' }}>
                        {risk.stockout_probability ? `${risk.stockout_probability.toFixed(1)}%` : 'N/A'}
                      </td>
                      <td style={{ padding: '0.75rem' }}>
                        <button className="btn btn-primary" style={{ fontSize: '0.85rem' }}>
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recommendations */}
      {risks.filter(r => r.risk_level === 'critical' || r.risk_level === 'high').length > 0 && (
        <div className="card" style={{ marginTop: '1.5rem' }}>
          <h2 className="card-title">Urgent Recommendations</h2>
          <ul style={{ paddingLeft: '1.5rem' }}>
            {risks
              .filter(r => r.risk_level === 'critical' || r.risk_level === 'high')
              .slice(0, 5)
              .map((risk, idx) => (
                <li key={idx} style={{ marginBottom: '0.5rem' }}>
                  <strong>{risk.part_name || risk.part_number}:</strong> {risk.recommended_action || 'Monitor closely'}
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default SupplyChain









