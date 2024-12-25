from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .docs import custom_openapi

def setup_api(app: FastAPI):
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Frontend dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup API documentation
    app.openapi = lambda: custom_openapi(app)

    # Create main router
    router = APIRouter(prefix="/api/v1")
    
    # Add all route groups
    router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    router.include_router(users_router, prefix="/users", tags=["Users"])
    router.include_router(messages_router, prefix="/messages", tags=["Messages"])
    
    app.include_router(router)
