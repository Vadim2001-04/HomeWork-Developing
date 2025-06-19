import React from 'react';
import { Link } from 'react-router-dom';

interface ProductCardProps {
  product: {
    id: number;
    name: string;
    price: number;
    rating: number;
    image?: string;
  };
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-105">
      <img
        src={product.image || "https://via.placeholder.com/300"}
        alt={product.name}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="text-lg font-semibold">{product.name}</h3>
        <p className="text-blue-600 font-bold">${product.price.toFixed(2)}</p>
        <p className="text-yellow-500">Rating: {product.rating}</p>
        <Link to={`/products/${product.id}`} className="mt-2 inline-block text-blue-600 hover:underline">
          View Details
        </Link>
      </div>
    </div>
  );
};

export default ProductCard;