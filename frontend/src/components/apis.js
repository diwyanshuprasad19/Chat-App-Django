// src/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api'; // Your backend API URL

export const register = async (phone, username, password) => {
  try {
    const response = await axios.post(`${API_URL}/register/`, { phone, username, password });
    return response.data;
  } catch (error) {
    console.error('Error registering user', error);
    throw error;
  }
};

export const login = async (phone, password) => {
  try {
    const response = await axios.post(`${API_URL}/login/`, { phone, password });
    return response.data;
  } catch (error) {
    console.error('Error logging in', error);
    throw error;
  }
};

export const logout = async () => {
  try {
    await axios.post(`${API_URL}/logout/`);
  } catch (error) {
    console.error('Error logging out', error);
    throw error;
  }
};
