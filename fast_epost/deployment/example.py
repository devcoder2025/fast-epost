from fast_epost.deployment.main import DeploymentOrchestrator

# Initialize the orchestrator
orchestrator = DeploymentOrchestrator()

# Deploy to staging
orchestrator.run_deployment(
    environment='staging',
    version='1.0.0'
)

# Check deployment metrics
metrics = orchestrator.monitor.get_stats()
print(f"Deployment Stats: {metrics}")
