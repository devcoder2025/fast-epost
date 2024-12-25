from flask import Flask
from flask_jwt_extended import JWTManager
from app.models import db
from config.config import Config
from app.utils.logger import setup_logger
from app.utils.error_handlers import register_error_handlers
from app.utils.rate_limit import limiter
from app.utils.cache import cache

jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Setup logging
    setup_logger(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import auth, packages, tracking, services
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(packages.bp, url_prefix='/api/packages')
    app.register_blueprint(tracking.bp, url_prefix='/api/tracking')
    app.register_blueprint(services.bp, url_prefix='/api/services')
    
    app.logger.info('Application startup complete')
    
    return app    return app