from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError

def validate_request(schema_class):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_class()
            try:
                data = request.get_json()
                validated_data = schema.load(data)
                return f(*args, **kwargs)
            except ValidationError as err:
                return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
        return decorated_function
    return decorator
