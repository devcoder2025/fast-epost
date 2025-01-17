import React, { useState } from 'react';
import axios from 'axios';

function UserProfile() {
  const [role, setRole] = useState('customer-service');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userProfileData = {
      role,
      email,
      password,
    };
    try {
      const response = await axios.post('/api/user/profile', userProfileData); // Adjust the API endpoint as needed
      console.log('Profile updated successfully:', response.data);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  return (
    <div id="user-profile" className="mb-4">
      <h2>User Profile</h2>
      <form id="profile-form" onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="userRole" className="form-label">Role</label>
          <select
            className="form-control"
            id="userRole"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
            aria-label="Select User Role"
          >
            <option value="customer-service">Customer Service</option>
            <option value="finance">Finance</option>
            <option value="supplier">Supplier</option>
            <option value="lawyer">Lawyer</option>
          </select>
        </div>
        <div className="mb-3">
          <label htmlFor="userEmail" className="form-label">Email address</label>
          <input
            type="email"
            className="form-control"
            id="userEmail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            aria-label="Email address"
          />
        </div>
        <div className="mb-3">
          <label htmlFor="userPassword" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="userPassword"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            aria-label="Password"
          />
        </div>
        <button type="submit" className="btn btn-primary">Save Profile</button>
      </form>
    </div>
  );
}

export default UserProfile;
