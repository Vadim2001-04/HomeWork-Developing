import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  rating: number;
}

const ProductDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get(`/products/${id}`);
        setProduct(response.data);
      } catch (error) {
        console.error('Error fetching product details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">{product.name}</h1>
      <div className="bg-white p-6 rounded shadow">
        <p className="mb-4">{product.description}</p>
        <p className="text-blue-600 font-bold text-xl">Price: ${product.price.toFixed(2)}</p>
        <p className="text-yellow-500">Rating: {product.rating}/5</p>
      </div>
    </div>
  );
};

export default ProductDetails;