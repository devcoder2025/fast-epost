class DeploymentTasks:
    @staticmethod
    async def run_tests():
        subprocess.run(['pytest'], check=True)
        
    @staticmethod
    async def build_docker():
        subprocess.run(['docker', 'build', '-t', 'fast-epost', '.'], check=True)
        
    @staticmethod
    async def deploy_heroku():
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
