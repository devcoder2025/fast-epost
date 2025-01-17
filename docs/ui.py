from flask import Blueprint, render_template
from .generator import SwaggerGenerator

docs_blueprint = Blueprint('docs', __name__)

class DocsUI:
    def __init__(self, swagger_gen: SwaggerGenerator):
        self.swagger = swagger_gen
        
    def render_docs(self):
        return render_template(
            'docs/index.html',
            api_spec=self.swagger.generate_spec()
        )
