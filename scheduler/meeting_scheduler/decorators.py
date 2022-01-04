"""
function decorators for scheduler app
"""
from functools import wraps


def user_required(fn):
    """
    Ensures that context contained user is available and not anonymous.
    """

    @wraps(fn)
    def wrapper(cls, root, info, **kwargs):
        """
        Wrapper function for the decorator.
        """
        user = info.context.user
        if user and user.is_anonymous:
            return cls(success=False, error="Could not validate the token credentials!")
        return fn(cls, root, info, **kwargs)

    return wrapper
