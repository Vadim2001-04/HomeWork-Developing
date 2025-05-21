import React, { useState } from 'react';
import axios from 'axios';

interface OrderItem {
  product_id: number;
  quantity: number;
}

const OrdersPage: React.FC = () => {
  const [orderItems, setOrderItems] = useState<OrderItem[]>([
    { product_id: 1, quantity: 2 },
  ]);

  const createOrder = async () => {
    await axios.post('/orders', { items: orderItems });
    alert('Order placed successfully!');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Place Your Order</h1>
      <div className="bg-white p-6 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
        <ul className="space-y-2">
          {orderItems.map((item, index) => (
            <li key={index} className="flex justify-between">
              <span>Product ID: {item.product_id}</span>
              <input
                type="number"
                value={item.quantity}
                onChange={(e) =>
                  setOrderItems([
                    ...orderItems.slice(0, index),
                    { ...item, quantity: parseInt(e.target.value) || 0 },
                    ...orderItems.slice(index + 1)
                  ])
                }
                className="w-16 border rounded px-2"
              />
            </li>
          ))}
        </ul>
        <button
          onClick={createOrder}
          className="mt-4 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Submit Order
        </button>
      </div>
    </div>
  );
};

export default OrdersPage;