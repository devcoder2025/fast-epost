from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Fast-EPost API",
        version="1.0.0",
        description="API documentation for Fast-EPost system",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
