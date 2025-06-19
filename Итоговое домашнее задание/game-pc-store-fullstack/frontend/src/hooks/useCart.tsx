import { useState, useEffect } from 'react';
import axios from 'axios';

interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

const useCart = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);

  const fetchCart = async () => {
    try {
      const response = await axios.get('/cart');
      setCartItems(response.data);
    } catch (error) {
      console.error('Error fetching cart:', error);
    }
  };

  const addToCart = async (productId: number, quantity: number = 1) => {
    await axios.post('/cart', { product_id: productId, quantity });
    fetchCart();
  };

  const removeFromCart = async (itemId: number) => {
    await axios.delete(`/cart/${itemId}`);
    fetchCart();
  };

  const updateQuantity = async (itemId: number, newQuantity: number) => {
    if (newQuantity <= 0) {
      await removeFromCart(itemId);
    } else {
      await axios.patch(`/cart/${itemId}`, { quantity: newQuantity });
      fetchCart();
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  return { cartItems, addToCart, removeFromCart, updateQuantity };
};

export default useCart;