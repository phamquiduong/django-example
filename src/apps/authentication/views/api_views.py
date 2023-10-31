from django.contrib.auth import authenticate, get_user_model
from django.http import HttpRequest, JsonResponse
from django.middleware import csrf
from django.utils import timezone

from apps.authentication.constants.api.api_code import APICode
from apps.authentication.decorator.require_login import require_login
from apps.authentication.helpers.token import AccessTokenHelper, RefreshTokenHelper
from decorators.api.require_http_methods import require_http_methods
from helpers.json import MyEncoder
from utils.api.exception import BadRequestException, UnauthorizedException
from utils.api.parse_request import parse_request

User = get_user_model()


@require_http_methods('GET')
def get_csrf_token(request: HttpRequest, *_, **__):
    return JsonResponse({'csrfmiddlewaretoken': csrf.get_token(request)})


@require_http_methods('POST', api_code=APICode.REGISTER)
def register(request: HttpRequest, *_, **__):
    data = parse_request(request)

    email = data.get('email', None)
    password = data.get('password', None)

    if not isinstance(email, str) or not isinstance(password, str) or not email or not password:
        raise BadRequestException(api_code=APICode.REGISTER, error_detail='Email or password not allowed')

    if User.objects.filter(email=email).exists():
        raise BadRequestException(api_code=APICode.REGISTER, error_detail='User already registered')

    user = User.objects.create_user(email=email, password=password)  # type: ignore

    return JsonResponse(user.dict(), encoder=MyEncoder)


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
        }, encoder=MyEncoder)

    raise UnauthorizedException(api_code=APICode.LOGIN, error_detail='Email or password incorrect')


@require_http_methods('POST', api_code=APICode.REFRESH)
def refresh_token(request: HttpRequest, *_, **__):
    data = parse_request(request)

    token = data.get('refresh_token', None)

    if not isinstance(token, str) or not token:
        raise BadRequestException(api_code=APICode.REFRESH, error_fields={'refresh_token': 'Required refresh token'})

    user_id = RefreshTokenHelper(api_code=APICode.REFRESH).auth(token=token)
    if user_id is None or not User.objects.filter(id=user_id).exists():
        raise BadRequestException(api_code=APICode.REFRESH, error_fields={'refresh_token': 'User does not exist'})

    return JsonResponse({
        'access_token': AccessTokenHelper(api_code=APICode.LOGIN).render(user_id=user_id),
        'refresh_token': RefreshTokenHelper(api_code=APICode.LOGIN).render(user_id=user_id),
    }, encoder=MyEncoder)


@require_http_methods('GET', api_code=APICode.GET_USER)
@require_login(api_code=APICode.GET_USER)
def get_user_info(___, user, *_, **__):
    return JsonResponse(user.dict(), encoder=MyEncoder)
