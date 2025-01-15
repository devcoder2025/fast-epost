import axios from 'axios';

const API_URL = 'https://api.fastepost.com'; // Replace with the actual API URL

// Simple in-memory cache
const cache = new Map();

export const fetchData = async (endpoint) => {
  if (cache.has(endpoint)) {
    return cache.get(endpoint); // Return cached data if available
  }
  
  try {
    const response = await axios.get(`${API_URL}/${endpoint}`);
    cache.set(endpoint, response.data); // Cache the fetched data
    return response.data;
  } catch (error) {
    console.error('Error fetching data from Fast Epost:', error);
    throw error;
  }
};

export const fetchUserProfile = async (userId) => {
  return await fetchData(`users/${userId}`);
  // Additional logic for user profile can be added here
};
