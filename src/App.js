import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UserProfile from './components/UserProfile';
import SupportSection from './components/SupportSection';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import Shipments from './components/Shipments';
import Settings from './components/Settings';
import LoadingScreen from './components/LoadingScreen';
import Logo from './components/Logo';
import './styles/styles.css';

function App() {
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [showAuth, setShowAuth] = useState(false);

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

  if (loading) {
    return <LoadingScreen />;
  }

  if (showAuth) {
    return (
      <div className="auth-container">
        <div className="background-logo">
          <Logo />
        </div>
        <div className="auth-content">
          {/* Login/Register components will go here */}
        </div>
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
