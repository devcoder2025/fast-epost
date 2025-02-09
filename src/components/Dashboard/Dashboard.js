import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import fetchData from '../fastEpostService'; // Import the fetchData function as default
import Shipments from './Shipments'; // Import the Shipments component
import logo from '../../logo.svg'; // Import the logo

function Dashboard() {
  const chartRef = useRef(null);
  const [shipmentData, setShipmentData] = useState([]);
  const [loading, setLoading] = useState(true); // Add loading state
  const [error, setError] = useState(null); // Add error state
  const chartInstance = useRef(null);
  const userId = '123'; // Replace with the actual user ID

  useEffect(() => {
    // Fetch shipment data
    const fetchShipmentData = async () => {
      setLoading(true); // Set loading to true before fetching
      try {
        const data = await fetchData(`shipments?userId=${userId}`); // Call the fetchData function with the endpoint
        setShipmentData(data);
      } catch (error) {
        setError('Failed to load shipment data. Please check your connection and try again.'); // Improved error message
        console.error('Error fetching shipment data:', error);
      } finally {
        setLoading(false); // Set loading to false after fetching
      }
    };

    fetchShipmentData();
  }, [userId]);

  useEffect(() => {
    // Only create chart if ref is available
    if (!chartRef.current) return;

    const ctx = chartRef.current.getContext('2d');
    if (!ctx) return;

    // Destroy existing chart if it exists
    if (chartInstance.current) {
      chartInstance.current.destroy();
      chartInstance.current = null;
    }

    // Create new chart with fetched data
    chartInstance.current = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: shipmentData.map(item => item.date), // Assuming shipmentData has a date field
        datasets: [{
          label: 'Shipments',
          data: shipmentData.map(item => item.count), // Assuming shipmentData has a count field
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
      }
    });

    // Cleanup function
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
        chartInstance.current = null;
      }
    };
  }, [shipmentData]); // Added shipmentData as a dependency

  // Ensure chart container has proper dimensions
  useEffect(() => {
    const container = document.querySelector('.chart-container');
    if (container) {
      container.style.width = '100%';
      container.style.height = '400px';
    }
  }, []);

  return (
    <div className="dashboard">
      <img src={logo} alt="Logo" style={{ width: '100px', marginBottom: '20px' }} /> {/* Display the logo */}
      {loading ? ( // Show loading indicator
        <p>Loading...</p>
      ) : error ? (
        <p>{error}</p> // Show improved error message
      ) : (
        <>
          <h2>Dashboard for User {userId}</h2>
          <div className="chart-container" style={{ position: 'relative', height: '40vh', width: '80vw' }}>
            <canvas ref={chartRef} id="shipmentChart"></canvas>
          </div>
          <Shipments /> {/* Include the Shipments component */}
        </>
      )}
    </div>
  );
}

export default Dashboard;
