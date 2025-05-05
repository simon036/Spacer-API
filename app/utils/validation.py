from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError

def validate_schema(schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                data = schema.load(request.get_json() or request.form)
            except ValidationError as err:
                return jsonify({"errors": err.messages}), 400
            return fn(data, *args, **kwargs)
        return wrapper
    return decorator