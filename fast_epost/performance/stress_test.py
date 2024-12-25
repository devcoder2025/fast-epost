import locust
from locust import HttpUser, task, between

class FastEpostUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def test_endpoints(self):
        self.client.get("/api/v1/status")
        self.client.post("/api/v1/data", json={"test": "data"})
