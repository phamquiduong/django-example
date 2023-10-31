from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.authentication.constants.api.api_code import APICode
from apps.authentication.helpers.token import AccessTokenHelper, RefreshTokenHelper
from utils.api.exception import BadRequestException, NotFoundException, UnauthorizedException

User = get_user_model()


def login(email, password):
    if not isinstance(email, str) or not email:
        raise BadRequestException(api_code=APICode.LOGIN, error_code=101, error_detail='Email is not valid',
                                  error_fields={'email': 'Email is multiple, null or empty'})

    if not isinstance(password, str) or not password:
        raise BadRequestException(api_code=APICode.LOGIN, error_code=111, error_detail='Password is not valid',
                                  error_fields={'password': 'Password is multiple, null or empty'})

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as exc:
        raise NotFoundException(api_code=APICode.LOGIN, error_code=101, error_detail='User is not found') from exc

    if not user.check_password(raw_password=password):
        raise UnauthorizedException(api_code=APICode.LOGIN, error_code=111, error_detail='Email or password incorrect')

    user.last_login = timezone.now()
    user.save()

    return {
        'access_token': AccessTokenHelper(api_code=APICode.LOGIN).render(user_id=user.id),  # type: ignore
        'refresh_token': RefreshTokenHelper(api_code=APICode.LOGIN).render(user_id=user.id),  # type: ignore
    }
