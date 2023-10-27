from http import HTTPStatus

from django.contrib.auth import authenticate
from django.http import HttpRequest, JsonResponse
from django.middleware import csrf
from django.utils import timezone

from apps.authentication.helpers.token import AccessTokenHelper, RefreshTokenHelper
from constants.api.api_code import APICode
from decorators.api.require_http_methods import require_http_methods
from utils.api.exception import BadRequestException
from utils.api.parse_request import parse_request


@require_http_methods('GET')
def get_csrf_token(request: HttpRequest, *_, **__):
    return JsonResponse({'csrfmiddlewaretoken': csrf.get_token(request)})


@require_http_methods('POST', api_code=APICode.LOGIN)
def login(request: HttpRequest, *_, **__):
    data = parse_request(request)

    email = data.get('email', None)
    password = data.get('password', None)

    if not isinstance(email, str) or not isinstance(password, str) or not email or not password:
        raise BadRequestException(api_code=APICode.LOGIN, error_detail='User name or password not allowed')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        user.last_login = timezone.now()
        user.save()
        return JsonResponse({
            'access_token': AccessTokenHelper(user.id).render(),  # type: ignore
            'refresh_token': RefreshTokenHelper(user.id).render(),  # type: ignore
        }, status=HTTPStatus.OK)

    return JsonResponse({})
