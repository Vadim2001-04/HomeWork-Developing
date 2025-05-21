import api from './api';

export const addToCart = async (productId: number, quantity: number) => {
  await api.post('/cart', { product_id: productId, quantity });
};