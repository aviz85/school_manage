import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import LoginScreen from './LoginScreen';
import WelcomeScreen from './WelcomeScreen';
import NotificationBar from './components/NotificationBar';
import MessageInbox from './components/MessageInbox';

const PrivateRoute: React.FC<{ element: React.ReactElement }> = ({ element }) => {
  const isAuthenticated = !!localStorage.getItem('accessToken');
  return isAuthenticated ? element : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <div className="App">
        <NotificationBar />
        <Routes>
          <Route path="/login" element={<LoginScreen />} />
          <Route path="/welcome" element={<PrivateRoute element={<WelcomeScreen />} />} />
          <Route path="/" element={<Navigate to="/welcome" />} />
          <Route path="/messages" element={<PrivateRoute element={<MessageInbox />} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
