import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import Shipments from './components/Shipments';
import Settings from './components/Settings';
import LoadingScreen from './components/LoadingScreen';
import './styles/styles.css';

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 2000);
  }, []);

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="container mt-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/shipments" element={<Shipments />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;