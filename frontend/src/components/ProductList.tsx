import React from 'react'
import { Product } from '../types/product'
import ProductCard from './ProductCard'

interface Props { products: Product[] }
const ProductList: React.FC<Props> = ({ products }) => {
  if (!products || products.length === 0) {
    return <p className="mt-6 text-center text-gray-400">No products tracked yet.</p>
  }
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
      {products.map((p, i) => <ProductCard key={i} {...p} />)}
    </div>
  )
}

export default ProductList
