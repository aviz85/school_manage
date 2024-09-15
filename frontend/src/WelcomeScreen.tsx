import React from 'react';
import { useNavigate } from 'react-router-dom';
import './WelcomeScreen.css';

const WelcomeScreen: React.FC = () => {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <div className="welcome-screen">
      <h1>Welcome to the School Management System</h1>
      <p>Hello, {username}! You've successfully logged in.</p>
      <div className="menu">
        <button onClick={() => navigate('/students')}>Manage Students</button>
        <button onClick={() => navigate('/teachers')}>Manage Teachers</button>
        <button onClick={() => navigate('/courses')}>Manage Courses</button>
      </div>
      <button className="logout-button" onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default WelcomeScreen;