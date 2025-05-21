import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Products from './pages/Products';
import Cart from './pages/Cart';
import Orders from './pages/Orders';
import Reviews from './pages/Reviews';
import ProductDetails from './pages/ProductDetails';
import Header from './components/Header';
import Footer from './components/Footer';

const App: React.FC = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:id" element={<ProductDetails />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/orders" element={<Orders />} />
        <Route path="/reviews" element={<Reviews />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;