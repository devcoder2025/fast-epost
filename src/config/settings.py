from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    RABBITMQ_URL: str
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
