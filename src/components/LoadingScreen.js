import React from 'react';
import Logo from './Logo';

function LoadingScreen() {
  return (
    <div className="loading-screen">
      <Logo />
      <div className="loading-spinner"></div>
    </div>
  );
}

export default LoadingScreen;
