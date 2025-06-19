import React from 'react';
import { render } from '@testing-library/react';
import ProductCard from '../components/ProductCard';

const mockProduct = {
  id: 1,
  name: 'Alienware Aurora R15',
  price: 3000,
  rating: 4.8,
  image: "https://via.placeholder.com/300",
};

test('renders product card with correct info', () => {
  const { getByText } = render(<ProductCard product={mockProduct} />);
  expect(getByText('Alienware Aurora R15')).toBeInTheDocument();
  expect(getByText('$3000.00')).toBeInTheDocument();
  expect(getByText('Rating: 4.8')).toBeInTheDocument();
});