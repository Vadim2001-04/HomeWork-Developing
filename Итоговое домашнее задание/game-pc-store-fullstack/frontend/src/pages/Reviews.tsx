import React, { useState } from 'react';
import axios from 'axios';

interface Review {
  id: number;
  user_id: number;
  product_id: number;
  text: string;
}

const ReviewsPage: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [productId, setProductId] = useState<number>(1);
  const [text, setText] = useState<string>('');

  const fetchReviews = async () => {
    const response = await axios.get(`/reviews?product_id=${productId}`);
    setReviews(response.data);
  };

  const submitReview = async () => {
    await axios.post('/reviews', { user_id: 1, product_id: productId, text });
    fetchReviews();
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Product Reviews</h1>
      <div className="bg-white p-6 rounded shadow">
        <div className="mb-4">
          <label className="block mb-2">Product ID:</label>
          <input
            type="number"
            value={productId}
            onChange={(e) => setProductId(parseInt(e.target.value))}
            className="border p-2 w-full"
          />
          <button
            onClick={fetchReviews}
            className="mt-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Load Reviews
          </button>
        </div>

        <ul className="space-y-2 mb-6">
          {reviews.map((review) => (
            <li key={review.id} className="border p-2 rounded">
              <p>{review.text}</p>
              <small className="text-gray-500">User ID: {review.user_id}</small>
            </li>
          ))}
        </ul>

        <div>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Write your review..."
            className="border p-2 w-full"
          />
          <button
            onClick={submitReview}
            className="mt-2 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Submit Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReviewsPage;