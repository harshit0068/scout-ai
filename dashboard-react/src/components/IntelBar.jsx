function IntelBar({ stats }) {
  if (!stats || stats.length === 0) {
    return <div className="intel-bar"><div className="intel-meta">No scan data yet</div></div>
  }

  return (
    <div className="intel-bar">
      {stats.map((s) => (
        <div className="intel-chip" key={s.source}>
          <div className="intel-name">{s.source}</div>
          <div className="intel-bar-track">
            <div className="intel-bar-fill" style={{ width: `${s.rate}%` }}></div>
          </div>
          <div className="intel-meta">{s.rate}% signal · {s.genuine}/{s.total} scanned</div>
        </div>
      ))}
    </div>
  )
}

export default IntelBar