from typing import Dict, List
import jinja2
import os

class SDKGenerator:
    def __init__(self, api_spec: Dict):
        self.api_spec = api_spec
        self.template_loader = jinja2.FileSystemLoader('templates/sdk')
        self.template_env = jinja2.Environment(loader=self.template_loader)
        
    def generate_python_client(self, output_dir: str):
        template = self.template_env.get_template('python_client.py.jinja')
        client_code = template.render(
            api_spec=self.api_spec,
            base_url="{{ base_url }}"
        )
        
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/client.py", "w") as f:
            f.write(client_code)
