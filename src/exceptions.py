from fastapi import status


class BaseAPIException(Exception):
    detail: str = "Internal server error"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class UsernameAlreadyExistsException(BaseAPIException):
    detail = 'User already exists'
    status_code = status.HTTP_409_CONFLICT


class IncorrectUserDataException(BaseAPIException):
    detail = 'Incorrect username or password'
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenNotFoundException(BaseAPIException):
    detail = 'Refresh token not found'
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidTokenException(BaseAPIException):
    detail = 'Invalid refresh token'
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenExpiredException(BaseAPIException):
    detail = 'Refresh token expired'
    status_code = status.HTTP_401_UNAUTHORIZED


class UnexpectedException(BaseAPIException):
    detail = 'Unexpected error occurred'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class DatabaseException(BaseAPIException):
    detail = 'Database operation failed'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class FormNotFoundExceprion(BaseAPIException):
    detail = 'Form not found'
    status_code = status.HTTP_404_NOT_FOUND
