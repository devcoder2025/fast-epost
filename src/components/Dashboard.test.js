import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

test('renders loading state', async () => {
  render(<Dashboard />);
  const loadingElement = await screen.findByText(/Loading.../i);
  expect(loadingElement).toBeInTheDocument();
});

test('renders error message when data fetch fails', () => {
    render(<Dashboard />);
    const errorElement = screen.getByText(/Failed to load shipment data. Please check your connection and try again./i);
    expect(errorElement).toBeInTheDocument();
});

test('renders error message when data fetch fails', () => {
    render(<Dashboard />);
    const errorElement = screen.getByText(/Failed to load shipment data. Please check your connection and try again./i);
    expect(errorElement).toBeInTheDocument();
});

test('renders error message when data fetch fails', () => {
    render(<Dashboard />);
    const errorElement = screen.getByText(/Failed to load shipment data. Please check your connection and try again./i);
    expect(errorElement).toBeInTheDocument();
});

test('renders error message when data fetch fails', () => {
    render(<Dashboard />);
    const errorElement = screen.getByText(/Failed to load shipment data. Please check your connection and try again./i);
    expect(errorElement).toBeInTheDocument();
});

test('renders error message when data fetch fails', () => {
    render(<Dashboard />);
    const errorElement = screen.getByText(/Failed to load shipment data. Please check your connection and try again./i);
    expect(errorElement).toBeInTheDocument();
});
