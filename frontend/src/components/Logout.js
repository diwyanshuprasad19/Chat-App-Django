// src/Logout.js
import React from 'react';
import { logout } from './api';

const Logout = () => {
  const handleLogout = async () => {
    try {
      await logout();
      // Redirect to login or show success message
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default Logout;
