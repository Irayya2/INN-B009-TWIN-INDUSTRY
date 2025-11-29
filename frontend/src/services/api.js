/**
 * API Client Service
 * Handles all API calls to the backend
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// Sensors API
export const sensorsAPI = {
  push: (data) => api.post('/sensors/push', data),
  getLatest: (machineId, limit = 100) => 
    api.get(`/sensors/latest/${machineId}?limit=${limit}`),
  getTimeframe: (machineId, hours = 24) =>
    api.get(`/sensors/timeframe/${machineId}?hours=${hours}`),
}

// Machines API
export const machinesAPI = {
  getAll: (status) => {
    const params = status ? { status } : {}
    return api.get('/machines/', { params })
  },
  getById: (machineId) => api.get(`/machines/${machineId}`),
  getStatusAll: () => api.get('/machines/status/all'),
  create: (machine) => api.post('/machines/', machine),
}

// Faults API
export const faultsAPI = {
  predict: (machineId) => api.get(`/faults/predict/${machineId}`),
  predictAll: () => api.get('/faults/predict/all'),
}

// Supply Chain API
export const supplyChainAPI = {
  getRisk: (partId) => api.get(`/supply/risk/${partId}`),
  getAllRisks: () => api.get('/supply/risk/all'),
  predictDelay: (supplierId) => api.get(`/supply/delay-prediction/${supplierId}`),
}

// Inventory API
export const inventoryAPI = {
  check: (lowStockOnly = false) => 
    api.get(`/inventory/check?low_stock_only=${lowStockOnly}`),
  getPart: (partId) => api.get(`/inventory/${partId}`),
}

// Alerts API
export const alertsAPI = {
  getAll: (status, severity, limit = 100) => {
    const params = {}
    if (status) params.status = status
    if (severity) params.severity = severity
    if (limit) params.limit = limit
    return api.get('/alerts/', { params })
  },
  getActive: () => api.get('/alerts/active'),
  acknowledge: (alertId, acknowledgedBy) => 
    api.post(`/alerts/${alertId}/acknowledge`, null, {
      params: { acknowledged_by: acknowledgedBy }
    }),
  resolve: (alertId) => api.post(`/alerts/${alertId}/resolve`),
}

// SOP API
export const sopAPI = {
  getTasks: (status, sopCode) => {
    const params = {}
    if (status) params.status = status
    if (sopCode) params.sop_code = sopCode
    return api.get('/sop/tasks', { params })
  },
  createTask: (task) => api.post('/sop/tasks', task),
  getTask: (taskId) => api.get(`/sop/tasks/${taskId}`),
  completeTask: (taskId, results, notes) =>
    api.post(`/sop/tasks/${taskId}/complete`, null, {
      params: { results, notes }
    }),
}

// Maintenance API
export const maintenanceAPI = {
  schedule: (request) => api.post('/maintenance/schedule', request),
  getLogs: (machineId, status, limit = 100) => {
    const params = {}
    if (machineId) params.machine_id = machineId
    if (status) params.status = status
    if (limit) params.limit = limit
    return api.get('/maintenance/logs', { params })
  },
}

export default api









