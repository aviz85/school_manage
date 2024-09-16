import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Statistics.css';

interface StatisticsData {
  totalStudents: number;
  totalTeachers: number;
  totalCourses: number;
}

const Statistics: React.FC = () => {
  const [stats, setStats] = useState<StatisticsData | null>(null);

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/statistics/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
          }
        });
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    };

    fetchStatistics();
  }, []);

  if (!stats) {
    return <div>Loading statistics...</div>;
  }

  return (
    <div className="statistics">
      <h2>School Statistics</h2>
      <div className="stat-item">
        <span className="stat-label">Total Students:</span>
        <span className="stat-value">{stats.totalStudents}</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">Total Teachers:</span>
        <span className="stat-value">{stats.totalTeachers}</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">Total Courses:</span>
        <span className="stat-value">{stats.totalCourses}</span>
      </div>
    </div>
  );
};

export default Statistics;