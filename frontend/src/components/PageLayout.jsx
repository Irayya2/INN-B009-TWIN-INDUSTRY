import React from 'react'
import '../App.css'

const PageLayout = ({ title, children, actions }) => {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>{title}</h1>
        </div>
        {actions && <div className="page-actions">{actions}</div>}
      </div>
      <div className="page-content">{children}</div>
    </div>
  )
}

export default PageLayout
