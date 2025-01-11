import React from 'react';
import { Card, CardContent, Switch, FormGroup, FormControlLabel } from '@mui/material';

function Settings() {
  return (
    <div className="settings">
      <h2>Settings</h2>
      <Card sx={{ margin: '20px', padding: '20px' }}>
        <CardContent sx={{ padding: '20px' }}>
          <FormGroup sx={{ gap: '15px' }}>
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Email Notifications"
              sx={{ marginBottom: '10px' }}
            />
            <FormControlLabel
              control={<Switch />}
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
