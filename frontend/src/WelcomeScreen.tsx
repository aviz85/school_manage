import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './WelcomeScreen.css';
import Statistics from './Statistics';
import SchoolIllustration from './SchoolIllustration';

const WelcomeScreen: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);
    } else {
      setError('User not authenticated');
    }
    setIsLoading(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('username');
    navigate('/login');
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="welcome-screen">
      <h1>Welcome to the School Management System</h1>
      <SchoolIllustration />
      <p>Hello, {username}! You've successfully logged in.</p>
      <Statistics />
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