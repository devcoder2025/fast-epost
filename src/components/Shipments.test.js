import React from 'react';
import { render, screen } from '@testing-library/react';
import Shipments from './Shipments';

test('renders loading state', async () => {
  render(<Shipments />);
  const loadingElement = await screen.findByText(/Loading.../i);
  expect(loadingElement).toBeInTheDocument();
});

test('renders error message when data fetch fails', () => {
  render(<Shipments />);
  const errorElement = screen.getByText(/Failed to load shipment data. Please check your connection and try again./i);
  expect(errorElement).toBeInTheDocument();
});


test('renders error message when data fetch fails', () => {
  render(<Shipments />);
  const errorElement = screen.getByText(/Failed to load shipment data. Please check your connection and try again./i);
  expect(errorElement).toBeInTheDocument();
});
