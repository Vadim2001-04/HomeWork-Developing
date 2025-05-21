import React, { useState } from 'react';
import { useCart } from '../hooks/useCart';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const CartPage: React.FC = () => {
  const { cartItems, removeFromCart, updateQuantity } = useCart();
  const [items, setItems] = useState(cartItems);

  useEffect(() => {
    setItems(cartItems);
  }, [cartItems]);

  const handleDragEnd = (result: any) => {
    if (!result.destination) return;
    const reorderedItems = Array.from(items);
    const [movedItem] = reorderedItems.splice(result.source.index, 1);
    reorderedItems.splice(result.destination.index, 0, movedItem);
    setItems(reorderedItems);
  };

  const totalPrice = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Your Cart</h1>
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="cart-items">
          {(provided) => (
            <ul {...provided.droppableProps} ref={provided.innerRef} className="space-y-4">
              {items.map((item, index) => (
                <Draggable key={item.id} draggableId={`item-${item.id}`} index={index}>
                  {(provided) => (
                    <li
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      className="bg-white p-4 rounded shadow flex justify-between items-center"
                    >
                      <div>
                        <h3 className="font-semibold">{item.name}</h3>
                        <p>${item.price.toFixed(2)} x {item.quantity}</p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          className="px-2 bg-gray-200 rounded"
                        >
                          -
                        </button>
                        <span>{item.quantity}</span>
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="px-2 bg-gray-200 rounded"
                        >
                          +
                        </button>
                        <button
                          onClick={() => removeFromCart(item.id)}
                          className="ml-2 text-red-500"
                        >
                          Remove
                        </button>
                      </div>
                    </li>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </ul>
          )}
        </Droppable>
      </DragDropContext>

      <div className="mt-6 text-right">
        <h2 className="text-xl font-bold">Total: ${totalPrice.toFixed(2)}</h2>
        <button className="mt-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Checkout
        </button>
      </div>
    </div>
  );
};

export default CartPage;