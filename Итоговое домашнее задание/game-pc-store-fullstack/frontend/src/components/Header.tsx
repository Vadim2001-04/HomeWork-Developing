import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="bg-blue-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">Game PC Store</h1>
        <nav>
          <ul className="flex space-x-4">
            <li><Link to="/" className="hover:underline">Home</Link></li>
            <li><Link to="/products" className="hover:underline">Products</Link></li>
            <li><Link to="/cart" className="hover:underline">Cart</Link></li>
            <li><Link to="/orders" className="hover:underline">Orders</Link></li>
            <li><Link to="/reviews" className="hover:underline">Reviews</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;