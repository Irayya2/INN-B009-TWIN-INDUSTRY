import React, { useState, useEffect } from 'react'
import '../App.css'

const images = [
  'https://source.unsplash.com/1600x900/?factory,industry',
  'https://source.unsplash.com/1600x900/?machinery,industrial',
  'https://source.unsplash.com/1600x900/?manufacturing,plant',
  'https://source.unsplash.com/1600x900/?assembly,line',
]

const HeroBanner = ({ interval = 5000 }) => {
  const [index, setIndex] = useState(0)

  useEffect(() => {
    const id = setInterval(() => {
      setIndex((i) => (i + 1) % images.length)
    }, interval)
    return () => clearInterval(id)
  }, [interval])

  return (
    <div className="hero-banner">
      <div className="hero-slides" aria-live="polite">
        {images.map((src, i) => (
          <div
            key={i}
            className={`hero-slide ${i === index ? 'active' : ''}`}
            style={{ backgroundImage: `url(${src})` }}
            role="img"
            aria-label={`Industrial image ${i + 1}`}
          />
        ))}
      </div>

      <div className="hero-overlay">
        <h2>Industrial Twin — Real-time Insights</h2>
        <p>Monitor machines, predict faults, and keep production running smoothly.</p>
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
