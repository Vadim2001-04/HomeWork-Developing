import React from 'react';

interface CartItemProps {
  item: {
    id: number;
    name: string;
    price: number;
    quantity: number;
  };
  onRemove: () => void;
  onUpdateQuantity: (newQty: number) => void;
}

const CartItem: React.FC<CartItemProps> = ({ item, onRemove, onUpdateQuantity }) => {
  return (
    <li className="flex justify-between items-center bg-white p-4 rounded shadow">
      <div>
        <h3 className="font-semibold">{item.name}</h3>
        <p>${item.price.toFixed(2)} x {item.quantity}</p>
      </div>
      <div className="flex space-x-2">
        <button onClick={() => onUpdateQuantity(item.quantity - 1)} className="px-2 bg-gray-200 rounded">
          -
        </button>
        <span>{item.quantity}</span>
        <button onClick={() => onUpdateQuantity(item.quantity + 1)} className="px-2 bg-gray-200 rounded">
          +
        </button>
        <button onClick={onRemove} className="ml-2 text-red-500">
          Remove
        </button>
      </div>
    </li>
  );
};

export default CartItem;