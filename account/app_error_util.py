from functools import wraps
from rest_framework.response import Response

# Assuming AppError is defined as in the previous example
from .app_error_util import AppError

def async_handler(view_func):
    @wraps(view_func)
    async def wrapped_view(*args, **kwargs):
        try:
            print('\nreq passed through async handler')
            return await view_func(*args, **kwargs)
        except AppError as app_error:
            # Handle specific application errors
            return Response({"error": str(app_error)}, status=app_error.status_code)
        except Exception as e:
            # Handle unexpected errors
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)
    
    return wrapped_view
