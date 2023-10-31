from django.http import HttpResponse, JsonResponse

from helpers.json import MyEncoder
from helpers.logger import logger
from utils.api.exception import APIException, MethodNotAllowedExeption


def require_http_methods(*request_methods: str, api_code: int = 0):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.method not in request_methods:
                return MethodNotAllowedExeption(api_code=api_code).get_response()

            try:
                response: JsonResponse | HttpResponse = func(request, *args, **kwargs)

                if isinstance(response, JsonResponse):
                    return response

                return JsonResponse({'data': response.getvalue()}, encoder=MyEncoder, status=response.status_code)

            except APIException as api_exc:
                logger.error(str(api_exc))
                return api_exc.get_response()

            except Exception as exc:
                logger.error(str(exc))
                return APIException(api_code=api_code, error_detail=str(exc)).get_response()

        return inner
    return decorator
