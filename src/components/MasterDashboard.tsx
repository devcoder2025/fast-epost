import React, { useState } from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { createTheme, ThemeProvider } from '@mui/material';
import Logo from '../assets/logo.svg';

// Create RTL theme
const rtlTheme = createTheme({
  direction: 'rtl',
  typography: {
    fontFamily: 'Arial, sans-serif',
  },
});

const MasterDashboard = () => {
  return (
    <ThemeProvider theme={rtlTheme}>
      <div className="master-dashboard" dir="rtl">
        <div className="dashboard-header">
          <img src={Logo} alt="Company Logo" className="dashboard-logo" />
          {/* Rest of your dashboard code */}
        </div>
      </div>
    </ThemeProvider>
  );
};
export default MasterDashboard;