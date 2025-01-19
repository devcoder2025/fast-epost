import React, { useState, useEffect } from 'react';
import Cache from './cache'; // Import the cache module
import { readFileAsync } from './fileOperations'; // Import async file operations
import AuthPage from './components/AuthPage';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UserProfile from './components/UserProfile';
import SupportSection from './components/SupportSection';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import Shipments from './components/Shipments';
import Settings from './components/Settings';
import LoadingScreen from './components/LoadingScreen';
import './styles/styles.css';

function App() {
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [showAuth, setShowAuth] = useState(false);
  const [userData, setUserData] = useState(null); // State to hold user data

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
      setShowAuth(true);
    }, 2000);
  }, []);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark-mode');
    document.querySelector('nav').classList.toggle('navbar-dark-mode');
  };

  useEffect(() => {
    const loadUserData = async () => {
      try {
        const data = await readFileAsync('path/to/user/data.json'); // Example path
        setUserData(data);
      } catch (error) {
        console.error('Error loading user data:', error);
      }
    };
    loadUserData();
  }, []);

  if (loading || !userData) {
    return <LoadingScreen onLoadingComplete={() => setLoading(false)} />;
  }

  if (showAuth) {
    return (
      <div>
        <h1>Welcome, {userData ? userData.name : 'User'}</h1> {/* Display user name */}
        <AuthPage />
      </div>
    );
  }

  return (
    <Router>
      <div className={`app ${darkMode ? 'dark-mode' : ''}`}>
        <Navbar onToggleTheme={toggleDarkMode} />
        <div className="main-layout">
          <div className="content-container">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/shipments" element={<Shipments />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/profile" element={<UserProfile />} />
              <Route path="/support" element={<SupportSection />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
