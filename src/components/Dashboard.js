import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';

function Dashboard() {
  const chartRef = useRef(null);

  useEffect(() => {
    // Destroy existing chart if it exists
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    // Create new chart
    const ctx = document.getElementById('shipmentChart').getContext('2d');
    chartRef.current = new Chart(ctx, {
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
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, []);

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="row">
        <div className="col-md-8">
          <canvas id="shipmentChart"></canvas>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;