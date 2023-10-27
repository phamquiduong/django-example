from django.contrib.auth import authenticate
from django.http import HttpRequest, JsonResponse
from django.middleware import csrf
from django.utils import timezone

from apps.authentication.constants.api.api_code import APICode
from apps.authentication.decorator.require_login import require_login
from apps.authentication.helpers.token import AccessTokenHelper, RefreshTokenHelper
from decorators.api.require_http_methods import require_http_methods
from utils.api.exception import BadRequestException, UnauthorizedException
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
        raise BadRequestException(api_code=APICode.LOGIN, error_detail='Email or password not allowed')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        user.last_login = timezone.now()
        user.save()
        return JsonResponse({
            'access_token': AccessTokenHelper(api_code=APICode.LOGIN).render(user_id=user.id),  # type: ignore
            'refresh_token': RefreshTokenHelper(api_code=APICode.LOGIN).render(user_id=user.id),  # type: ignore
        })

    raise UnauthorizedException(api_code=APICode.LOGIN, error_detail='Email or password incorrect')


@require_http_methods('GET', api_code=APICode.GET_USER)
@require_login(api_code=APICode.GET_USER)
def get_user_info(___, user, *_, **__):
    return JsonResponse(user.dict())
