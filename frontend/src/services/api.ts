const API_BASE = 'import.meta.env.VITE_API_BASE_URL'
//const API_BASE = 'http://127.0.0.1:5000/'
export async function trackProduct(productName: string) {
  const res = await fetch(`${API_BASE}/track`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product: productName }) // 
  })
  if (!res.ok) throw new Error('Network error')
  return res.json()
}
