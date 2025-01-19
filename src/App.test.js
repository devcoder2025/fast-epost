import { render, screen } from '@testing-library/react';
import App from './App';

test('renders loading screen initially', () => {
  render(<App />);
  const loadingElement = screen.getByText(/loading/i);
  expect(loadingElement).toBeInTheDocument();
});

test('renders navbar after loading', async () => {
  render(<App />);
  const navbarElement = await screen.findByRole('navigation');
  expect(navbarElement).toBeInTheDocument();
});

test('renders dashboard after authentication', async () => {
  render(<App />);
  const dashboardElement = await screen.findByText(/dashboard/i);
  expect(dashboardElement).toBeInTheDocument();
});
