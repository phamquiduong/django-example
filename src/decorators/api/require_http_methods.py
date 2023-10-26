from django.http import JsonResponse

from helpers.logger import logger
from utils.api.exception import APIException, MethodNotAllowedExeption


def require_http_methods(*request_methods: str, api_code: int = 0):
    def decorator(func):

        def inner(request, *args, **kwargs):
            if request.method not in request_methods:
                return MethodNotAllowedExeption(api_code=api_code).get_response()

            try:
                response = func(request, *args, **kwargs)

                if isinstance(response, JsonResponse):
                    return response

                return JsonResponse(status=response.status_code, data={})

            except APIException as api_exc:
                logger.error(str(api_exc))
                return api_exc.get_response()

            except Exception as exc:
                logger.error(str(exc))
                return APIException(api_code=api_code).get_response()

        return inner

    return decorator
