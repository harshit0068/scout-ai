function Header({ count, lastSync }) {
  return (
    <header className="header">
      <div className="wordmark">
        <span className="live-dot"></span>
        SCOUT
      </div>
      <div className="status-line">
        <div>{count} signal{count !== 1 ? 's' : ''}</div>
        <div>last sync <span className="signal-text">{lastSync || '—'}</span></div>
      </div>
    </header>
  )
}

export default Header