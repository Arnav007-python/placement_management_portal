from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(role):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator
