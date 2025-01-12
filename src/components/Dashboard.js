import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

function Dashboard() {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

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

    // Create new chart
    chartInstance.current = new Chart(ctx, {

      type: 'bar',
      data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        datasets: [{
          label: 'Shipments',
          data: [12, 19, 3, 5, 2],
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
  }, []);

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
      <h2>Dashboard</h2>
      <div className="chart-container">
        <canvas ref={chartRef} id="shipmentChart"></canvas>
      </div>
    </div>
  );
}

export default Dashboard;
