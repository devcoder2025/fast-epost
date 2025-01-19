import React, { useEffect, useState } from 'react';
import { fetchUserProfile } from '../fastEpostService';

function Profile() {
  const [userData, setUserData] = useState(null);
  const userId = '123'; // Replace with the actual user ID

  useEffect(() => {
    const getUserProfile = async () => {
      try {
        const data = await fetchUserProfile(userId);
        setUserData(data);
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    };

    getUserProfile();
  }, [userId]);

  return (
    <div className="profile">
      <h2>User Profile</h2>
      {userData ? (
        <div className="profile-details">
          <p><strong>Name:</strong> {userData.name}</p>
          <p><strong>Email:</strong> {userData.email}</p>
          <p><strong>Phone:</strong> {userData.phone}</p>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
}

export default Profile;
