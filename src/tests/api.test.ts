describe('API Tests', () => {
  it('should handle successful requests', async () => {
    const response = await api.get('/endpoint');
    expect(response.status).toBe(200);
  });

  it('should handle errors gracefully', async () => {
    const response = await api.get('/invalid');
    expect(response.status).toBe(404);
  });
});
