import React from 'react';
import Switch from '@mui/material/Switch';

interface FeatureToggleProps {
  name: string;
  enabled: boolean;
  onToggle: (enabled: boolean) => void;
}

const FeatureToggle = ({ name, enabled, onToggle }: FeatureToggleProps) => (
  <div className="feature-toggle">
    <span>{name}</span>
    <Switch checked={enabled} onChange={(e) => onToggle(e.target.checked)} />
  </div>
);
