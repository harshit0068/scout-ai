import { useState } from 'react'

function ringColor(pct) {
  if (pct >= 70) return 'var(--signal)'
  if (pct >= 40) return 'var(--cold)'
  return '#6B4A4A'
}

function decodeEntities(text) {
  const el = document.createElement('textarea')
  el.innerHTML = text
  return el.value
}

function stripHtml(text) {
  return text.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim()
}

function LeadCard({ lead }) {
  const [expanded, setExpanded] = useState(false)

  const pct = Math.round((lead.confidenceScore || 0) * 100)
  const color = ringColor(pct)
  const circumference = 100.5
  const offset = circumference - (circumference * pct) / 100
  const idTag = String(lead.id).padStart(3, '0')
  const cleanText = decodeEntities(stripHtml(lead.text || ''))

  return (
    <div className="transmission">
      <div className="t-top">
        <div className="ring-wrap">
          <svg className="ring" viewBox="0 0 40 40">
            <circle className="ring-bg" cx="20" cy="20" r="16"></circle>
            <circle
              className="ring-fg"
              cx="20" cy="20" r="16"
              style={{ strokeDashoffset: offset, stroke: color }}
            ></circle>
          </svg>
          <span className="ring-label">{pct}%</span>
        </div>
        <div className="t-info">
          <div className="t-meta">
            <span className="t-id">#{idTag}</span>
            <span className="t-source-badge">{lead.source || 'unknown'}</span>
            <span className="t-author">{lead.author}</span>
            <a className="t-link" href={lead.url} target="_blank" rel="noreferrer">source ↗</a>
          </div>
          <div className="t-summary">{lead.summary || '(no summary available)'}</div>
        </div>
      </div>
      <div className={`t-text ${expanded ? 'expanded' : ''}`}>{cleanText}</div>
      <button className="t-expand" onClick={() => setExpanded(!expanded)}>
        expand raw post ▾
      </button>
    </div>
  )
}

export default LeadCard