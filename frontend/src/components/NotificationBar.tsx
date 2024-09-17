import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { messageService } from '../services/messageService';
import './NotificationBar.css';

const NotificationBar: React.FC = () => {
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const fetchUnreadCount = async () => {
      try {
        const response = await messageService.getUnreadCount();
        setUnreadCount(response.data.unread_count);
      } catch (error) {
        console.error('Error fetching unread count:', error);
      }
    };

    fetchUnreadCount();
    const interval = setInterval(fetchUnreadCount, 60000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="notification-bar">
      <Link to="/welcome" className="home-button">Home</Link>
      <Link to="/messages" className="messages-button">
        Messages <span className="unread-count">{unreadCount}</span>
      </Link>
    </div>
  );
};

export default NotificationBar;