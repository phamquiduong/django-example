from http import HTTPStatus

from django.http import JsonResponse

from helpers.json import JsonHelper, MyEncoder


class APIException(Exception):
    def __init__(self,
                 status_code: HTTPStatus | int = HTTPStatus.INTERNAL_SERVER_ERROR,
                 api_code: int = 0,
                 error_code: int = 0,
                 error_detail: str | None = None,
                 error_fields: dict[str, str] | None = None) -> None:

        self.status_code = status_code
        self.api_code = api_code
        self.error_code = error_code
        self.error_detail = error_detail or (status_code.description if isinstance(status_code, HTTPStatus) else '')
        self.error_fields = error_fields

        super().__init__(self.error_detail)

    def dict(self):
        error_dict = {
            'status_code': self.status_code,
            'error_code': f'E-{self.status_code:03d}-{self.api_code:03d}-{self.error_code:03d}',
            'error_detail': self.error_detail,
        }
        if self.error_fields is not None:
            error_dict['error_fields'] = self.error_fields
        return error_dict

    def dumps(self):
        return JsonHelper.encode(self.dict())

    def get_response(self):
        return JsonResponse(self.dict(), encoder=MyEncoder, status=self.status_code)
