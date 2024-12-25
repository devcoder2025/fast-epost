from fast_epost.deployment.main import DeploymentOrchestrator
from fast_epost.deployment.config.environments import DEPLOYMENT_CONFIGS

def run_full_deployment():
    orchestrator = DeploymentOrchestrator()
    
    # Deploy to staging first
    orchestrator.run_deployment(
        environment='staging',
        version='1.0.0',
        config=DEPLOYMENT_CONFIGS['staging']
    )
    
    # If staging successful, deploy to production
    if orchestrator.monitor.get_stats()['staging']['status'] == 'success':
        orchestrator.run_deployment(
            environment='production',
            version='1.0.0',
            config=DEPLOYMENT_CONFIGS['production']
        )

if __name__ == '__main__':
    run_full_deployment()
