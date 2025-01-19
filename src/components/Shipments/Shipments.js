import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import axios from 'axios';

const columns = [
  { field: 'id', headerName: 'ID', width: 90 },
  { field: 'origin', headerName: 'Origin', width: 130 },
  { field: 'destination', headerName: 'Destination', width: 130 },
  { field: 'status', headerName: 'Status', width: 130 },
  { field: 'date', headerName: 'Date', width: 130 },
];

function Shipments() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true); // Add loading state
  const [error, setError] = useState(null); // Add error state

  useEffect(() => {
    // Fetch shipments data
    const fetchShipmentsData = async () => {
      setLoading(true); // Set loading to true before fetching
      try {
        const response = await axios.get('/api/shipments'); // Adjust the API endpoint as needed
        setShipments(response.data);
      } catch (error) {
        setError('Failed to load shipment data. Please check your connection and try again.'); // Improved error message
        console.error('Error fetching shipment data:', error);
      } finally {
        setLoading(false); // Set loading to false after fetching
      }
    };

    fetchShipmentsData();
  }, []);

  return (
    <div style={{ 
      height: '60vh', 
      width: '100%',
      padding: '0 15px',
      overflow: 'auto'
    }}>
      <h2>Shipments</h2>
      {loading ? (
        <p>Loading...</p> // Show loading indicator
      ) : error ? (
        <p>{error}</p> // Show improved error message
      ) : (
        <DataGrid
          rows={shipments}
          columns={columns}
          pageSize={5}
          rowsPerPageOptions={[5]}
          checkboxSelection
          disableSelectionOnClick
          autoHeight
          sx={{
            '& .MuiDataGrid-cell': {
              fontSize: '0.875rem',
            },
            '@media (max-width: 768px)': {
              '& .MuiDataGrid-cell': {
                fontSize: '0.75rem',
              },
            }
          }}
        />
      )}
    </div>
  );
}

export default Shipments;
