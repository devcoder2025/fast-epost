import { getUserProfile, getShipments } from './clientSDK';
import axios from 'axios';

jest.mock('axios');

describe('Client SDK', () => {
  it('fetches user profile successfully', async () => {
    const userId = '123';
    const userData = { name: 'John Doe', email: 'john@example.com', phone: '123-456-7890' };
    
    axios.get.mockResolvedValue({ data: userData });

    const result = await getUserProfile(userId);
    expect(result).toEqual(userData);
    expect(axios.get).toHaveBeenCalledWith('https://api.fastepost.com/users/123');
  });

  it('fetches shipment data successfully', async () => {
    const userId = '123';
    const shipmentData = [{ date: '2023-01-01', count: 10 }, { date: '2023-01-02', count: 15 }];
    
    axios.get.mockResolvedValue({ data: shipmentData });

    const result = await getShipments(userId);
    expect(result).toEqual(shipmentData);
    expect(axios.get).toHaveBeenCalledWith('https://api.fastepost.com/shipments', { params: { userId } });
  });

  it('handles errors when fetching user profile', async () => {
    const userId = '123';
    axios.get.mockRejectedValue(new Error('Error fetching user profile'));

    await expect(getUserProfile(userId)).rejects.toThrow('Error fetching user profile');
  });

  it('handles errors when fetching shipment data', async () => {
    const userId = '123';
    axios.get.mockRejectedValue(new Error('Error fetching shipment data'));

    await expect(getShipments(userId)).rejects.toThrow('Error fetching shipment data');
  });
});
