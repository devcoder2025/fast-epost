import React from 'react';
import { Card, CardContent, Switch, FormGroup, FormControlLabel } from '@mui/material';

function Settings() {
  return (
    <div className="settings">
      <h2>Settings</h2>
      <Card>
        <CardContent>
          <FormGroup>
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Email Notifications"
            />
            <FormControlLabel
              control={<Switch />}
              label="Dark Mode"
            />
          </FormGroup>
        </CardContent>
      </Card>
    </div>
  );
}

export default Settings;
