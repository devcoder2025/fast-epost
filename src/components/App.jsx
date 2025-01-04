import React from 'react';
import { ThemeProvider } from './context/ThemeContext';
import ErrorBoundary from './components/ErrorBoundary';

const App = () => {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <Router>
          <Navigation />
          <Routes />
        </Router>
      </ThemeProvider>
    </ErrorBoundary>
  );
};
