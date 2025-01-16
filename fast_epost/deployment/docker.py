class DockerManager:  
    def __init__(self, base_path: str):  
        self.client = docker.from_env()  
        self.base_path = base_path  # Store base path for Docker operations

    def build_image(self, tag: str):
        return self.client.images.build(path=self.base_path, tag=tag)
    def __init__(self):
        self.client = docker.from_env()
        
    def push_image(self, tag: str):
        return self.client.images.push(tag)
        
    def push_image(self, tag: str):
        return self.client.images.push(tag)
