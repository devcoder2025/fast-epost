import os
from typing import Dict, Any

class HerokuConfig:
    @staticmethod
    def get_database_url() -> str:
        return os.environ.get('DATABASE_URL')
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        return {
            'SECRET_KEY': os.environ.get('SECRET_KEY'),
            'AWS_ACCESS_KEY': os.environ.get('AWS_ACCESS_KEY'),
            'AWS_SECRET_KEY': os.environ.get('AWS_SECRET_KEY'),
            'S3_BUCKET': os.environ.get('S3_BUCKET'),
            'DEBUG': False,
            'PORT': int(os.environ.get('PORT', 5000))
        }
