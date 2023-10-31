from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse

from apps.authentication import services
from apps.authentication.constants.api.api_code import APICode
from apps.authentication.decorator.require_login import require_login
from decorators.api.require_http_methods import require_http_methods
from helpers.json import MyEncoder
from utils.api.parse_request import parse_request

User = get_user_model()


@require_http_methods('GET')
def get_csrf_token_view(request: HttpRequest, *_, **__):
    return JsonResponse(services.get_csrf_token(request))


@require_http_methods('POST', api_code=APICode.REGISTER)
def register_view(request: HttpRequest, *_, **__):
    data = parse_request(request)
    email = data.get('email', None)
    password = data.get('password', None)
    return JsonResponse(services.register(email=email, password=password), encoder=MyEncoder)


@require_http_methods('POST', api_code=APICode.LOGIN)
def login_view(request: HttpRequest, *_, **__):
    data = parse_request(request)
    email = data.get('email', None)
    password = data.get('password', None)
    return JsonResponse(services.login(email=email, password=password), encoder=MyEncoder)


@require_http_methods('POST', api_code=APICode.REFRESH)
def refresh_token_view(request: HttpRequest, *_, **__):
    data = parse_request(request)
    token = data.get('refresh_token', None)
    return JsonResponse(services.refresh_token(token=token), encoder=MyEncoder)


@require_http_methods('GET', api_code=APICode.GET_USER)
@require_login(api_code=APICode.GET_USER)
def get_user_info_view(___, user, *_, **__):
    return JsonResponse(user.dict(), encoder=MyEncoder)
