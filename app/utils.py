from flask_login import current_user
from functools import wraps
from flask import redirect, url_for, flash

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('Access denied.')
                return redirect(url_for('main.index'))  # Use blueprint endpoint
            return f(*args, **kwargs)
        return decorated_function
    return decorator