import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import '../App.css'

const images = [
  'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=1600&h=900&fit=crop',
  'https://images.unsplash.com/photo-1565793298595-6a94f57e2834?w=1600&h=900&fit=crop',
  'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1600&h=900&fit=crop',
  'https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600&h=900&fit=crop',
]

const HeroBanner = ({ interval = 7000 }) => {
  const [index, setIndex] = useState(0)
  const navigate = useNavigate()

  useEffect(() => {
    const id = setInterval(() => {
      setIndex((i) => (i + 1) % images.length)
    }, interval)
    return () => clearInterval(id)
  }, [interval])

  const handleViewMachineHealth = () => {
    navigate('/machine-health')
  }

  const handleLearnMore = () => {
    navigate('/')
    // Scroll to top or show info modal
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="hero-banner">
      <div className="hero-slides" aria-live="polite">
        {images.map((src, i) => (
          <div
            key={i}
            className={`hero-slide ${i === index ? 'active' : ''}`}
            style={{ 
              backgroundImage: `url(${src})`,
              backgroundColor: '#1a1a2e'
            }}
            role="img"
            aria-label={`Industrial image ${i + 1}`}
          />
        ))}
      </div>

      <div className="hero-overlay">
        <h2>Industrial Twin — Predictive Maintenance</h2>
        <p>Real-time machine health & proactive maintenance</p>
        <div style={{ marginTop: '1rem', display: 'flex', gap: '0.75rem' }}>
          <button 
            className="btn btn-primary"
            onClick={handleViewMachineHealth}
            style={{ 
              backgroundColor: '#007BFF',
              color: 'white',
              border: 'none',
              padding: '0.5rem 1.5rem',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = '#0056b3'}
            onMouseLeave={(e) => e.target.style.backgroundColor = '#007BFF'}
          >
            View Machine Health
          </button>
          <button 
            className="btn btn-outline"
            onClick={handleLearnMore}
            style={{ 
              backgroundColor: 'transparent',
              color: 'white',
              border: '2px solid white',
              padding: '0.5rem 1.5rem',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s'
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = 'rgba(255,255,255,0.2)'
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = 'transparent'
            }}
          >
            Learn More
          </button>
        </div>
      </div>

      <div className="hero-dots" aria-hidden>
        {images.map((_, i) => (
          <button
            key={i}
            className={`dot ${i === index ? 'active' : ''}`}
            onClick={() => setIndex(i)}
            aria-label={`Go to slide ${i + 1}`}
          />
        ))}
      </div>
    </div>
  )
}

export default HeroBanner
