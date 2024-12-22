from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        app.logger.error(f'HTTP error occurred: {error}')
        response = {
            'error': error.name,
            'message': error.description,
            'status_code': error.code
        }
        return jsonify(response), error.code

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        app.logger.error(f'Database error occurred: {error}')
        response = {
            'error': 'Database Error',
            'message': 'An internal database error occurred',
            'status_code': 500
        }
        return jsonify(response), 500

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        app.logger.error(f'Unexpected error occurred: {error}')
        response = {
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }
        return jsonify(response), 500
