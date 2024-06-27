from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import abort, jsonify
from app.status_code import StatusCodes
from flask_jwt_extended import jwt_required, get_jwt_identity

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user_role = current_user.get('role')

            if user_role not in allowed_roles:
                response = jsonify({
                    'status': StatusCodes.Forbidden.value,
                    'message': 'Access forbidden: insufficient permissions'
                })
                response.status_code = StatusCodes.Forbidden.value
                return response
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
