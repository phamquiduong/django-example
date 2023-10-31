from django.contrib.auth import authenticate
from django.utils import timezone

from apps.authentication.constants.api.api_code import APICode
from apps.authentication.helpers.token import AccessTokenHelper, RefreshTokenHelper
from utils.api.exception import BadRequestException, UnauthorizedException


def login(email, password):
    if not isinstance(email, str) or not isinstance(password, str) or not email or not password:
        raise BadRequestException(api_code=APICode.LOGIN, error_detail='Email or password not allowed')

    user = authenticate(email=email, password=password)

    if user is None:
        raise UnauthorizedException(api_code=APICode.LOGIN, error_detail='Email or password incorrect')

    user.last_login = timezone.now()
    user.save()

    return {
        'access_token': AccessTokenHelper(api_code=APICode.LOGIN).render(user_id=user.id),  # type: ignore
        'refresh_token': RefreshTokenHelper(api_code=APICode.LOGIN).render(user_id=user.id),  # type: ignore
    }
