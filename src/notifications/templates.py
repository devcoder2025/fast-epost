
from jinja2 import Template
from typing import Dict

class NotificationTemplates:
    BUILD_SUCCESS = Template("""
        <h2>Build Successful</h2>
        <p>Project: {{ project_name }}</p>
        <p>Version: {{ version }}</p>
        <p>Build Time: {{ build_time }}s</p>
        <p>Artifacts: {{ artifacts }}</p>
    """)

    BUILD_FAILURE = Template("""
        <h2>Build Failed</h2>
        <p>Project: {{ project_name }}</p>
        <p>Error: {{ error }}</p>
        <p>Log: {{ log }}</p>
    """)

    SYSTEM_ALERT = Template("""
        <h2>System Alert</h2>
        <p>Type: {{ alert_type }}</p>
        <p>Message: {{ message }}</p>
        <p>Timestamp: {{ timestamp }}</p>
    """)

    def render(self, template_name: str, context: Dict) -> str:
        template = getattr(self, template_name)
        return template.render(**context)
