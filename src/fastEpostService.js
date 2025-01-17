import axios from 'axios';

const API_URL = 'https://api.fastepost.com'; // Replace with the actual API URL

export const fetchData = async (endpoint) => {
  try {
    const response = await axios.get(`${API_URL}/${endpoint}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching data from Fast Epost:', error);
    throw error;
  }
};

// Add more functions as needed to interact with the Fast Epost API
