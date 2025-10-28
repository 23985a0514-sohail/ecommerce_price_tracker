import React, { useState } from 'react'
import SearchBar from '../components/SearchBar'
import ProductList from '../components/ProductList'
import { Product } from '../types/product'
import { trackProduct } from '../services/api'

const Home: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (q: string) => {
    setLoading(true); setError(null)
    try {
      const res = await trackProduct(q)
      setProducts(res)
    } catch (e: any) {
      setError('Failed to fetch products')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <SearchBar onSearch={handleSearch} />
      {loading && <p className="mt-4 text-center">Fetching products...</p>}
      {error && <p className="mt-4 text-red-400 text-center">{error}</p>}
      <ProductList products={products} />
    </div>
  )
}

export default Home
