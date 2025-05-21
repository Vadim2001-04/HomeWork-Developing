import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import CartPage from '../pages/Cart';

jest.mock('../hooks/useCart', () => ({
  useCart: () => ({
    cartItems: [
      { id: 1, name: 'Alienware Aurora R15', price: 3000, quantity: 2 },
    ],
    removeFromCart: jest.fn(),
    updateQuantity: jest.fn(),
  }),
}));

describe('Cart Page', () => {
  test('renders cart items correctly', () => {
    render(<CartPage />);
    expect(screen.getByText(/Alienware Aurora R15/i)).toBeInTheDocument();
    expect(screen.getByText(/\$3000 x 2/i)).toBeInTheDocument();
  });

  test('calls remove function when remove button is clicked', () => {
    render(<CartPage />);
    const removeButton = screen.getByText(/Remove/i);
    fireEvent.click(removeButton);
    expect(jest.fn()).toHaveBeenCalledTimes(1);
  });

  test('updates item quantity when +/- buttons are clicked', () => {
    render(<CartPage />);
    const minusButton = screen.getByText(/-/i);
    const plusButton = screen.getByText(/\+/i);

    fireEvent.click(minusButton);
    fireEvent.click(plusButton);

    expect(jest.fn()).toHaveBeenCalledTimes(2);
  });
});