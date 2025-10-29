const API_URL = import.meta.env.VITE_API_URL;

export const trackProduct = async (product: string) => {
  const res = await fetch(`${API_URL}/track`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product }),
  });
  if (!res.ok) throw new Error(`Failed to fetch product data (Status: ${res.status})`);
  return await res.json();
};

export const getPriceHistory = async (product: string) => {
  const res = await fetch(`${API_URL}/history/${encodeURIComponent(product)}`);
  if (!res.ok) throw new Error(`Failed to fetch price history (Status: ${res.status})`);
  return await res.json();
};
