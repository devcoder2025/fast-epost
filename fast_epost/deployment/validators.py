class DeploymentValidator:
    def validate_config(self, config: Dict) -> bool:
        required = ['environment', 'version', 'dependencies']
        return all(key in config for key in required)
        
    def check_environment(self, env: str) -> bool:
        return all(var in os.environ for var in ['DATABASE_URL', 'SECRET_KEY'])
