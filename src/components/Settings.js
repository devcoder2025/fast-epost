import React, { useState } from 'react';
import { Card, CardContent, Switch, FormGroup, FormControlLabel } from '@mui/material';

function Settings() {
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  const handleEmailNotificationsChange = (event) => {
    setEmailNotifications(event.target.checked);
    // Save email notification preference (e.g., to local storage or API)
  };

  const handleDarkModeChange = (event) => {
    setDarkMode(event.target.checked);
    document.body.classList.toggle('dark-mode', event.target.checked);
    // Save dark mode preference (e.g., to local storage or API)
  };

  return (
    <div className="settings">
      <h2>Settings</h2>
      <Card sx={{ margin: '20px', padding: '20px' }}>
        <CardContent sx={{ padding: '20px' }}>
          <FormGroup sx={{ gap: '15px' }}>
            <FormControlLabel
              control={<Switch checked={emailNotifications} onChange={handleEmailNotificationsChange} />}
              label="Email Notifications"
              sx={{ marginBottom: '10px' }}
            />
            <FormControlLabel
              control={<Switch checked={darkMode} onChange={handleDarkModeChange} />}
              label="Dark Mode"
              sx={{ marginBottom: '10px' }}
            />
          </FormGroup>
        </CardContent>
      </Card>
    </div>
  );
}

export default Settings;
