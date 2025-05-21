import React from 'react';
import ProductCard from '../components/ProductCard';
import { useProducts } from '../hooks/useProducts';

const Home: React.FC = () => {
  const { products, isLoading } = useProducts();

  if (isLoading) {
    return <div className="text-center py-8">Loading products...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Featured PCs</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default Home;