const API_URL = 'import.meta.env.VITE_API_URL';

export async function trackProduct(product: string) {
  try {
    const response = await fetch(`${API_URL}/track`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product }),
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errText}`);
    }

    return await response.json();
  } catch (error: any) {
    console.error("Error in trackProduct:", error);
    throw new Error("Failed to fetch product data");
  }
}
