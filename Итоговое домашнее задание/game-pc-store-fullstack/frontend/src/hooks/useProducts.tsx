import { useState, useEffect } from 'react';
import axios from 'axios';

interface Product {
  id: number;
  name: string;
  price: number;
  rating: number;
  image?: string;
}

const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/products');
        setProducts(response.data);
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return { products, isLoading };
};

export default useProducts;