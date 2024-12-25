class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        
    def build_image(self, tag: str):
        return self.client.images.build(path='.', tag=tag)
        
    def push_image(self, tag: str):
        return self.client.images.push(tag)
