import axios from 'axios';

const API_URL = 'https://api.fastepost.com'; // Replace with the actual API URL

// Simple in-memory cache
const cache = new Map();
let requestCount = 0; // Counter for requests
const requestLimit = 100; // Limit of requests
const timeWindow = 60000; // Time window in milliseconds (1 minute)
let lastRequestTime = Date.now(); // Timestamp of the last request

// Function to set the JWT token in the headers
export const setAuthToken = (token) => {
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete axios.defaults.headers.common['Authorization'];
  }
};

// Function to check rate limiting
const checkRateLimit = () => {
  const currentTime = Date.now();
  if (currentTime - lastRequestTime > timeWindow) {
    requestCount = 0; // Reset the count after the time window
    lastRequestTime = currentTime;
  }
  requestCount++;
  if (requestCount > requestLimit) {
    throw new Error('Rate limit exceeded. Please try again later.');
  }
};

// Function to fetch data from the API
export const fetchData = async (endpoint) => {
  checkRateLimit(); // Check rate limit before making the request

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
