from rest_framework.exceptions import APIException
from rest_framework import status

# Define error codes and messages
class ErrorCodes:
    DEFAULT_ERROR = 1000
    VALIDATION_ERROR = 1001
    AUTHENTICATION_ERROR = 1002
    FORBIDDEN_ERROR = 1003
    CONFLICT = 1004
    DATABASE_ERROR = 1005
    ORDER_ERROR = 1006
    TRANSACTION_ERROR = 1007

class AppError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Internal Server Error'

    def __init__(self, app_code=ErrorCodes.DEFAULT_ERROR, detail=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        self.app_code = app_code
        super().__init__(detail, status_code)

    @classmethod
    def validation(cls, detail=None):
        return cls(app_code=ErrorCodes.VALIDATION_ERROR, detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def authentication(cls, detail=None):
        return cls(app_code=ErrorCodes.AUTHENTICATION_ERROR, detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def forbidden(cls, detail=None):
        return cls(app_code=ErrorCodes.FORBIDDEN_ERROR, detail=detail, status_code=status.HTTP_403_FORBIDDEN)

    @classmethod
    def conflict(cls, detail=None):
        return cls(app_code=ErrorCodes.CONFLICT, detail=detail, status_code=status.HTTP_409_CONFLICT)

    @classmethod
    def database(cls, detail=None):
        return cls(app_code=ErrorCodes.DATABASE_ERROR, detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def order(cls, detail=None):
        return cls(app_code=ErrorCodes.ORDER_ERROR, detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def transaction(cls, detail=None):
        return cls(app_code=ErrorCodes.TRANSACTION_ERROR, detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def test_error(cls, detail=None):
        return cls(app_code='1000', detail=detail, status_code=status.HTTP_400_BAD_REQUEST)
