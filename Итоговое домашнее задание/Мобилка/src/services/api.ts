import axios from 'axios';

const API_URL = 'https://jsonplaceholder.typicode.com/posts';

export const fetchPosts = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const fetchPost = async (id: string) => {
  const response = await axios.get(`${API_URL}/${id}`);
  return response.data;
};