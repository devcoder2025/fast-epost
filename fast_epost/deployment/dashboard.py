from flask import Blueprint, render_template
from .monitor import DeploymentMonitor

deployment_dashboard = Blueprint('deployment', __name__)

class DeploymentDashboard:
    def __init__(self):
        self.monitor = DeploymentMonitor()
        
    def get_deployment_status(self):
        return {
            'deployments': self.monitor.get_stats(),
            'success_rate': self.calculate_success_rate(),
            'average_duration': self.calculate_avg_duration()
        }
        
    def render_dashboard(self):
        return render_template(
            'deployment/dashboard.html',
            stats=self.get_deployment_status()
        )
