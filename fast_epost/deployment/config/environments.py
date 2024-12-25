DEPLOYMENT_CONFIGS = {
    'staging': {
        'url': 'https://staging.fast-epost.com',
        'replicas': 2,
        'resources': {
            'cpu': '500m',
            'memory': '512Mi'
        }
    },
    'production': {
        'url': 'https://fast-epost.com',
        'replicas': 3,
        'resources': {
            'cpu': '1000m',
            'memory': '1Gi'
        }
    }
}
