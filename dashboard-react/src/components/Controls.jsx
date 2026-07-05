function Controls({ search, setSearch, sortBy, setSortBy, onRefresh }) {
  return (
    <div className="controls">
      <input
        type="text"
        placeholder="Filter by author, source, or keyword..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        <option value="confidence">Highest confidence</option>
        <option value="newest">Newest first</option>
      </select>
      <button onClick={onRefresh}>Refresh</button>
    </div>
  )
}

export default Controls