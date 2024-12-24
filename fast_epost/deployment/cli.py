import click

@click.command()
@click.option('--env', type=click.Choice(['staging', 'production']))
@click.option('--version', required=True)
def deploy(env, version):
    orchestrator = DeploymentOrchestrator()
    orchestrator.run_deployment(env, version)

if __name__ == '__main__':
    deploy()
