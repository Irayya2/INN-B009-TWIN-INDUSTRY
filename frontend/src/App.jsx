import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import MachineHealth from './pages/MachineHealth'
import SupplyChain from './pages/SupplyChain'
import Alerts from './pages/Alerts'
import SOPManager from './pages/SOPManager'
import MaintenanceScheduler from './pages/MaintenanceScheduler'
import './App.css'
import SensorTestInput from "./pages/SensorTestInput"


function Navigation() {
  const location = useLocation()
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/machine-health', label: 'Machine Health', icon: '⚙️' },
    { path: '/supply-chain', label: 'Supply Chain', icon: '📦' },
    { path: '/alerts', label: 'Alerts', icon: '🔔' },
    { path: '/sop-manager', label: 'SOP Manager', icon: '📋' },
    { path: '/maintenance', label: 'Maintenance', icon: '🔧' },
    { path: '/test-input', label: 'Test Machine', icon: '🧪' },

  ]

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <h1>🏭 Industrial Twin</h1>
        <span className="subtitle">Predictive Maintenance System</span>
      </div>
      <div className="nav-links">
        {navItems.map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={location.pathname === item.path ? 'active' : ''}
          >
            <span className="nav-icon">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </div>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/machine-health" element={<MachineHealth />} />
            <Route path="/supply-chain" element={<SupplyChain />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/sop-manager" element={<SOPManager />} />
            <Route path="/maintenance" element={<MaintenanceScheduler />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App











