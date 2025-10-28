import React, { useState } from 'react'

interface Props { onSearch: (q: string) => void }

const SearchBar: React.FC<Props> = ({ onSearch }) => {
  const [q, setQ] = useState('')
  return (
    <form onSubmit={e => { e.preventDefault(); onSearch(q) }} className="flex gap-2">
      <input value={q} onChange={e=>setQ(e.target.value)} className="w-full p-3 rounded-l-md bg-gray-800 border border-gray-700" placeholder="Search product e.g. iPhone 13" />
      <button type="submit" className="px-4 bg-indigo-600 rounded-r-md">Track</button>
    </form>
  )
}

export default SearchBar
