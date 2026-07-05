import { useState, useEffect } from 'react'
import Header from './components/Header'
import Controls from './components/Controls'
import IntelBar from './components/IntelBar'
import LeadCard from './components/LeadCard'

const API_BASE = 'https://scout-ai-backend-07sn.onrender.com/api/leads'

function App() {
  const [leads, setLeads] = useState([])
  const [stats, setStats] = useState([])
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState('confidence')
  const [lastSync, setLastSync] = useState(null)
  const [error, setError] = useState(false)

  const loadLeads = async () => {
    try {
      const res = await fetch(API_BASE)
      const data = await res.json()
      setLeads(data)
      setLastSync(new Date().toLocaleTimeString())
      setError(false)
    } catch (e) {
      console.error(e)
      setError(true)
    }
  }

  const loadStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/stats`)
      const data = await res.json()
      setStats(data)
    } catch (e) {
      console.error(e)
    }
  }

  const handleRefresh = () => {
    loadLeads()
    loadStats()
  }

  useEffect(() => {
    handleRefresh()
  }, [])

  const filtered = leads.filter((lead) => {
    const q = search.toLowerCase()
    return (
      (lead.author || '').toLowerCase().includes(q) ||
      (lead.source || '').toLowerCase().includes(q) ||
      (lead.text || '').toLowerCase().includes(q)
    )
  })

  const sorted = sortBy === 'newest' ? [...filtered].reverse() : filtered

  return (
    <div>
      <Header count={leads.length} lastSync={lastSync} />
      <IntelBar stats={stats} />
      <main>
        <Controls
          search={search}
          setSearch={setSearch}
          sortBy={sortBy}
          setSortBy={setSortBy}
          onRefresh={handleRefresh}
        />

        {error && (
          <div className="empty">Can't reach the backend.<br />Is it running on :8080?</div>
        )}

        {!error && sorted.length === 0 && (
          <div className="empty">No genuine signals yet. Run your scrapers to populate this.</div>
        )}

        {!error && sorted.map((lead) => (
          <LeadCard key={lead.id} lead={lead} />
        ))}
      </main>
    </div>
  )
}

export default App