from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest

from apps.authentication.helpers.token import AccessTokenHelper
from utils.api.exception import UnauthorizedException

User = get_user_model()


def require_login(api_code: int = 0):
    def decorator(func):
        def inner(request: HttpRequest, *args, **kwargs):
            access_token = request.headers.get(settings.API_AUTH_HEADER, None)

            if not access_token:
                raise UnauthorizedException(api_code=api_code, error_detail='Access token is empty')

            user_id = AccessTokenHelper(api_code=api_code).auth(token=access_token)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist as not_exist_exc:
                raise UnauthorizedException(api_code=api_code, error_detail='User does not exist') from not_exist_exc

            return func(request, user, *args, **kwargs)
        return inner
    return decorator
