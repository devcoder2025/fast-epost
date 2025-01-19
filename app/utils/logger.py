import logging
import os
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(app, log_directory='logs'):
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    # Set up file handler
    file_handler = RotatingFileHandler(
        f'{log_directory}/fastpost.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    
    # Set up formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Set up app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info('FastPost startup')
