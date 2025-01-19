import axios from 'axios';

const API_URL = 'https://api.fastepost.com'; // Replace with the actual API URL

export const getUserProfile = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/users/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export const getShipments = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/shipments`, {
      params: { userId }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching shipment data:', error);
    throw error;
  }
};

// Add more functions as needed to interact with the Fast Epost API
