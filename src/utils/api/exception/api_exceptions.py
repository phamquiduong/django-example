from http import HTTPStatus

from utils.api.exception.exception_base import APIException


class BadRequestException(APIException):
    def __init__(self, api_code: int = 0, error_code: int = 0, error_detail: str | None = None,
                 error_fields: dict[str, str | list[str]] | None = None) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST,
                         api_code=api_code, error_code=error_code, error_detail=error_detail, error_fields=error_fields)


class UnauthorizedException(APIException):
    def __init__(self, api_code: int = 0, error_code: int = 0, error_detail: str | None = None) -> None:
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED,
                         api_code=api_code, error_code=error_code, error_detail=error_detail)


class ForbiddenException(APIException):
    def __init__(self, api_code: int = 0, error_code: int = 0, error_detail: str | None = None) -> None:
        super().__init__(status_code=HTTPStatus.FORBIDDEN,
                         api_code=api_code, error_code=error_code, error_detail=error_detail)


class NotFoundException(APIException):
    def __init__(self, api_code: int = 0, error_code: int = 0, error_detail: str | None = None) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND,
                         api_code=api_code, error_code=error_code, error_detail=error_detail)


class MethodNotAllowedException(APIException):
    def __init__(self, api_code: int = 0, error_code: int = 0, error_detail: str | None = None) -> None:
        super().__init__(status_code=HTTPStatus.METHOD_NOT_ALLOWED,
                         api_code=api_code, error_code=error_code, error_detail=error_detail)


class ConflictException(APIException):
    def __init__(self, api_code: int = 0, error_code: int = 0, error_detail: str | None = None) -> None:
        super().__init__(status_code=HTTPStatus.CONFLICT,
                         api_code=api_code, error_code=error_code, error_detail=error_detail)
