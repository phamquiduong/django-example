from django.contrib.auth import get_user_model

from apps.authentication.constants.api.api_code import APICode
from apps.authentication.helpers.token import AccessTokenHelper, RefreshTokenHelper
from utils.api.exception import BadRequestException, NotFoundException

User = get_user_model()


def refresh_token(token):
    if not isinstance(token, str) or not token:
        raise BadRequestException(api_code=APICode.REFRESH, error_code=100,
                                  error_fields={'refresh_token': 'Required refresh token'})

    user_id = RefreshTokenHelper(api_code=APICode.REFRESH).auth(token=token)
    if user_id is None or not User.objects.filter(id=user_id).exists():
        raise NotFoundException(api_code=APICode.REFRESH, error_code=100, error_detail='User not found')

    return {
        'access_token': AccessTokenHelper(api_code=APICode.REFRESH).render(user_id=user_id),
        'refresh_token': RefreshTokenHelper(api_code=APICode.REFRESH).render(user_id=user_id),
    }
