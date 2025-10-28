import React from 'react'
import { Product } from '../types/product'

const ProductCard: React.FC<Product> = ({ name, price, site }) => {
  return (
    <div className="card">
      <h3 className="font-semibold text-lg">{name}</h3>
      <p className="text-green-400 font-bold mt-2">₹{price}</p>
      {site && <p className="text-sm text-gray-400 mt-1">Source: {site}</p>}
    </div>
  )
}

export default ProductCard
