#!/bin/bash

# Navigate to the main project directory and install dependencies
echo "Installing main project dependencies..."
npm install

# Navigate to the frontend project directory and install dependencies
echo "Installing frontend project dependencies..."
cd free-react-dashboard && npm install

echo "All dependencies installed successfully."
