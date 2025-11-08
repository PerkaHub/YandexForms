from fastapi import status


class BaseAPIException(Exception):
    detail: str = "Internal server error"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class UsernameAlreadyExistsException(BaseAPIException):
    detail = "User already exists"
    status_code = status.HTTP_409_CONFLICT


class IncorrectUserDataException(BaseAPIException):
    detail = "Incorrect username or password"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenNotFoundException(BaseAPIException):
    detail = "Refresh token not found"
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidTokenException(BaseAPIException):
    detail = "Invalid refresh token"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenExpiredException(BaseAPIException):
    detail = "Refresh token expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class UnexpectedException(BaseAPIException):
    detail = "Unexpected error occurred"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class DatabaseException(BaseAPIException):
    detail = "Database operation failed"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ShortUsernameException(BaseAPIException):
    detail = "Username too short"
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT


class FormNotFoundExceprion(BaseAPIException):
    detail = "Form not found"
    status_code = status.HTTP_404_NOT_FOUND


class FieldNotFoundException(BaseAPIException):
    def __init__(self, field_id: int):
        self.detail = f"Field with id {field_id} not found in form"
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.detail, self.status_code)


class TextAnswerRequiredException(BaseAPIException):
    def __init__(self, field_id: int):
        self.detail = f"Text answer required for field {field_id}"
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.detail, self.status_code)


class OptionIDNotAllowedException(BaseAPIException):
    def __init__(self, field_id: int):
        self.detail = f"Option ID not allowed for text field {field_id}"
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.detail, self.status_code)


class OptionIDRequiredException(BaseAPIException):
    def __init__(self, field_id: int):
        self.detail = f"Option ID required for field {field_id}"
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.detail, self.status_code)


class TextNotAllowedException(BaseAPIException):
    def __init__(self, field_type, field_id: int):
        self.detail = f"Text not allowed for {field_type} field {field_id}"
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.detail, self.status_code)


class OptionNotFoundException(BaseAPIException):
    def __init__(self, option_id: int, field_id: int):
        self.detail = (
            f"Option with id {option_id} " f"not found for field {field_id}"
        )
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.detail, self.status_code)


class RequiredFieldException(BaseAPIException):
    def __init__(self, question_text: str, field_id: int):
        self.detail = (
            f'Required field "{question_text}" '
            f"(id: {field_id}) must be answered"
        )
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.detail, self.status_code)
