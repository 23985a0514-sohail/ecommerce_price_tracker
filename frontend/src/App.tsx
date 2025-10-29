import React, { useState } from "react";
import { trackProduct, getPriceHistory } from "./services/api";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-800 p-3 rounded-lg shadow-lg border border-teal-400">
          <p className="text-sm text-gray-300">{`Date: ${label}`}</p>
          <p className="text-teal-400 font-semibold">{`₹${payload[0].value}`}</p>
        </div>
      );
    }
    return null;
  };

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

  const handleViewHistory = async () => {
    try {
      const data = await getPriceHistory(query);
      setHistory(data);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-4xl font-bold mb-6">
        <span className="text-yellow-400">E-Commerce</span> Price Tracker 🛒
      </h1>

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
        <div className="mt-6 bg-gray-800 rounded-xl p-6 shadow-lg w-full max-w-2xl">
          <h2 className="text-xl font-semibold mb-3 text-red-300">Results from Flipkart</h2>
          <div className="max-h-96 overflow-y-auto space-y-2">
            {results.flipkart?.length > 0 ? (
              results.flipkart.map((item: any, idx: number) => (
                <div key={idx} className="bg-gray-700 p-3 rounded-lg flex justify-between">
                  <span>{item.name}</span>
                  <span className="font-semibold text-green-400">₹{item.price}</span>
                </div>
              ))
            ) : (
              <p className="text-gray-400">No products found.</p>
            )}
          </div>

          <button
            onClick={handleViewHistory}
            className="mt-4 bg-green-600 px-5 py-2 rounded-lg hover:bg-green-700"
          >
            View Price History
          </button>
        </div>
      )}

      {history.length > 0 && (
        <div className="mt-8 bg-gray-800 p-6 rounded-xl w-full max-w-3xl">
          <h2 className="text-xl font-semibold mb-4 text-yellow-400">
            Price History for "{query}"
          </h2>

          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" tick={{ fill: "#ccc", fontSize: 12 }} />
              <YAxis tick={{ fill: "#ccc", fontSize: 12 }} />
              <Tooltip content={<CustomTooltip />} />
              <Line type="monotone" dataKey="price" stroke="#00ffcc" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default App;
