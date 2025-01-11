import React, { useEffect } from 'react';
import { Chart } from 'chart.js/auto';

function Dashboard() {
  useEffect(() => {
    const ctx = document.getElementById('shipmentChart').getContext('2d');
    new Chart(ctx, {
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
  }, []);

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="row">
        <div className="col-md-8">
          <canvas id="shipmentChart"></canvas>
        </div>
        <div className="col-md-4">
          {/* Add additional widgets/stats here */}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
