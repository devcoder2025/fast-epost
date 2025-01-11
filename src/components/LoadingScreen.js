import React from 'react';
import Logo from './Logo';

function LoadingScreen() {
  return (
    <div className="loading-screen">
      <Logo className="loading-logo" />
      <div className="loading-spinner"></div>
    </div>
  );
}

export default LoadingScreen;
