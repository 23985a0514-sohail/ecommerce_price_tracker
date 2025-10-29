const API_URL = 'import.meta.env.VITE_API_URL'

export const trackProduct = async (product: string) => {
  const response = await fetch(`${API_URL}/track`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch");
  }

  return response.json();
};
