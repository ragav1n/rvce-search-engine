import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
      setResults(res.data.results);
    } catch (error) {
      console.error("Search failed:", error);
      setResults([]);
    }
    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4 text-center">RVCE Site Search</h1>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search documents, PDFs, pages..."
          className="w-full p-4 rounded-lg border border-gray-700 bg-gray-800 placeholder-gray-400 text-white focus:outline-none focus:ring focus:border-blue-500"
        />

        {loading && <p className="mt-4 text-gray-400">Searching...</p>}

        {!loading && results.length > 0 && (
          <div className="mt-6 space-y-6">
            {results.map((r, i) => (
              <div key={i} className="bg-gray-800 p-4 rounded-lg shadow">
                <a href={r.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 text-lg font-semibold hover:underline">
                  {r.title || r.url}
                </a>
                <p className="text-gray-300 text-sm mt-2" dangerouslySetInnerHTML={{ __html: r.snippet }}></p>
              </div>
            ))}
          </div>
        )}

        {!loading && results.length === 0 && query && (
          <p className="mt-4 text-gray-400">No results found.</p>
        )}
      </div>
    </div>
  );
}
