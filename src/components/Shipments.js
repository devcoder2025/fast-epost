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

  useEffect(() => {
    // Fetch shipments data
    const fetchShipmentsData = async () => {
      try {
        const response = await axios.get('/api/shipments'); // Adjust the API endpoint as needed
        setShipments(response.data);
      } catch (error) {
        console.error('Error fetching shipment data:', error);
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
    </div>
  );
}

export default Shipments;
