from functools import wraps


def user_required(fn):
    @wraps(fn)
    def wrapper(cls, root, info, **kwargs):
        user = info.context.user
        if user and user.is_anonymous:
            return cls(success=False, error="Could not validate the token credentials!")
        return fn(cls, root, info, **kwargs)

    return wrapper
