import React, { useState } from "react";
import { trackProduct } from "./services/api";

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTrack = async () => {
    if (!query) return;
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await trackProduct(query);
      setResults(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-4xl font-bold mb-6"><span className="text-yellow-400">E-Commerce</span> Price Tracker 🛒</h1>

      <div className="flex space-x-2 w-full max-w-md">
        <input
          type="text"
          placeholder="Enter product name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-grow p-3 rounded-lg text-black"
        />
        <button
          onClick={handleTrack}
          disabled={loading}
          className="bg-blue-600 px-5 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Tracking..." : "Track"}
        </button>
      </div>

      {error && <p className="mt-4 text-red-400">{error}</p>}

      {results && (
  <div className="mt-6 bg-gray-800 rounded-xl p-6 shadow-lg w-full max-w-2xl relative overflow-hidden">
    <h2 className="text-xl font-semibold mb-3 text-red-300">Results from Flipkart</h2>

    {/* Sticky Highlighted Header */}
    <div className="grid grid-cols-2 font-semibold text-gray-100 bg-blue-700/90 
                    border border-gray-600 rounded-lg px-3 py-2 mb-2 shadow-md 
                    sticky top-0 z-10 backdrop-blur-sm">
      <span>Product Name</span>
      <span className="text-right">Price</span>
    </div>

    {/* Scrollable Product List */}
    <div className="max-h-96 overflow-y-auto space-y-2">
      {results.flipkart && results.flipkart.length > 0 ? (
        results.flipkart.map((item: any, idx: number) => (
          <div
            key={idx}
            className="bg-gray-700 p-3 rounded-lg flex justify-between items-center hover:bg-gray-600 transition"
          >
            <span>{item.name}</span>
            <span className="font-semibold text-green-400">{item.price}</span>
          </div>
        ))
      ) : (
        <p className="text-gray-400">No products found.</p>
      )}
    </div>
  </div>
)}
    </div>
  );
}

export default App;
