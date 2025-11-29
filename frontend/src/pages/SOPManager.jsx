import React, { useState, useEffect } from 'react'
import { sopAPI } from '../services/api'
import '../App.css'
import PageLayout from '../components/PageLayout'

const SOP_CODES = {
  'SOP-MAINT-01': 'Daily Machine Health Check',
  'SOP-MAINT-02': 'Predictive Maintenance Scheduling',
  'SOP-SC-04': 'Spare Parts Inventory Check',
  'SOP-RISK-07': 'Downtime & Risk Assessment Report',
}

function SOPManager() {
  const [tasks, setTasks] = useState([])
  const [filter, setFilter] = useState({ status: '', sopCode: '' })
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newTask, setNewTask] = useState({
    sop_code: '',
    task_name: '',
    description: '',
    scheduled_date: '',
    priority: 'medium',
  })

  useEffect(() => {
    loadTasks()
  }, [filter])

  const loadTasks = async () => {
    try {
      const data = await sopAPI.getTasks(filter.status || undefined, filter.sopCode || undefined)
      setTasks(data || [])
      setLoading(false)
    } catch (error) {
      console.error('Error loading SOP tasks:', error)
      setLoading(false)
    }
  }

  const handleCreateTask = async (e) => {
    e.preventDefault()
    try {
      await sopAPI.createTask({
        ...newTask,
        scheduled_date: new Date(newTask.scheduled_date).toISOString(),
      })
      setShowCreateForm(false)
      setNewTask({
        sop_code: '',
        task_name: '',
        description: '',
        scheduled_date: '',
        priority: 'medium',
      })
      loadTasks()
    } catch (error) {
      console.error('Error creating task:', error)
      alert('Failed to create task')
    }
  }

  const handleCompleteTask = async (taskId) => {
    try {
      await sopAPI.completeTask(taskId, 'Task completed via dashboard', '')
      loadTasks()
    } catch (error) {
      console.error('Error completing task:', error)
      alert('Failed to complete task')
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#28a745'
      case 'in_progress':
        return '#17a2b8'
      case 'overdue':
        return '#dc3545'
      default:
        return '#6c757d'
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  const pendingTasks = tasks.filter(t => t.status === 'pending').length
  const overdueTasks = tasks.filter(t => t.status === 'overdue').length

  return (
    <PageLayout
      title="SOP Workflow Manager"
      actions={(
        <button className="btn btn-primary" onClick={() => setShowCreateForm(!showCreateForm)}>
          {showCreateForm ? 'Cancel' : '+ Create Task'}
        </button>
      )}
    >

      {/* Create Task Form */}
      {showCreateForm && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h2 className="card-title">Create New SOP Task</h2>
          <form onSubmit={handleCreateTask}>
            <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: '1fr 1fr' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  SOP Code *
                </label>
                <select
                  required
                  value={newTask.sop_code}
                  onChange={(e) => setNewTask({ ...newTask, sop_code: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                >
                  <option value="">Select SOP...</option>
                  {Object.entries(SOP_CODES).map(([code, name]) => (
                    <option key={code} value={code}>
                      {code} - {name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Task Name *
                </label>
                <input
                  type="text"
                  required
                  value={newTask.task_name}
                  onChange={(e) => setNewTask({ ...newTask, task_name: e.target.value })}
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
                  value={newTask.scheduled_date}
                  onChange={(e) => setNewTask({ ...newTask, scheduled_date: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Priority
                </label>
                <select
                  value={newTask.priority}
                  onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div style={{ gridColumn: '1 / -1' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                  Description
                </label>
                <textarea
                  value={newTask.description}
                  onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd', minHeight: '100px' }}
                />
              </div>
            </div>
            <button type="submit" className="btn btn-primary" style={{ marginTop: '1rem' }}>
              Create Task
            </button>
          </form>
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Total Tasks</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>{tasks.length}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Pending</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#6c757d' }}>{pendingTasks}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Overdue</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#dc3545' }}>{overdueTasks}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Completed</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#28a745' }}>
            {tasks.filter(t => t.status === 'completed').length}
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
            <option value="">All</option>
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="overdue">Overdue</option>
          </select>

          <label style={{ fontWeight: '600', marginLeft: '1rem' }}>SOP Code:</label>
          <select
            value={filter.sopCode}
            onChange={(e) => setFilter({ ...filter, sopCode: e.target.value })}
            style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
          >
            <option value="">All</option>
            {Object.keys(SOP_CODES).map(code => (
              <option key={code} value={code}>{code}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Tasks List */}
      <div className="card">
        <h2 className="card-title">SOP Tasks</h2>
        {tasks.length === 0 ? (
          <p style={{ color: '#666', textAlign: 'center', padding: '2rem' }}>
            No tasks found
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                  <th style={{ padding: '0.75rem' }}>SOP Code</th>
                  <th style={{ padding: '0.75rem' }}>Task Name</th>
                  <th style={{ padding: '0.75rem' }}>Status</th>
                  <th style={{ padding: '0.75rem' }}>Priority</th>
                  <th style={{ padding: '0.75rem' }}>Scheduled</th>
                  <th style={{ padding: '0.75rem' }}>Assigned To</th>
                  <th style={{ padding: '0.75rem' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => (
                  <tr key={task.id} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '0.75rem' }}>{task.sop_code}</td>
                    <td style={{ padding: '0.75rem', fontWeight: '600' }}>{task.task_name}</td>
                    <td style={{ padding: '0.75rem' }}>
                      <span
                        style={{
                          padding: '0.25rem 0.75rem',
                          borderRadius: '12px',
                          fontSize: '0.85rem',
                          fontWeight: '500',
                          backgroundColor: getStatusColor(task.status) + '33',
                          color: getStatusColor(task.status),
                        }}
                      >
                        {task.status.replace(/_/g, ' ').toUpperCase()}
                      </span>
                    </td>
                    <td style={{ padding: '0.75rem' }}>{task.priority}</td>
                    <td style={{ padding: '0.75rem' }}>
                      {new Date(task.scheduled_date).toLocaleString()}
                    </td>
                    <td style={{ padding: '0.75rem' }}>{task.assigned_to || 'Unassigned'}</td>
                    <td style={{ padding: '0.75rem' }}>
                      {task.status !== 'completed' && (
                        <button
                          className="btn btn-primary"
                          onClick={() => handleCompleteTask(task.id)}
                          style={{ fontSize: '0.85rem' }}
                        >
                          Complete
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default SOPManager









