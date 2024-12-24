@deployment_dashboard.route('/api/metrics')
def get_metrics():
    return jsonify(dashboard.get_deployment_status())

@deployment_dashboard.route('/api/latest')
def get_latest_deployment():
    stats = dashboard.get_deployment_status()
    return jsonify(stats['deployments'][-1])
