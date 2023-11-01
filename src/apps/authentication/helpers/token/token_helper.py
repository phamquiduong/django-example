from datetime import timedelta

from django.utils import timezone

from apps.authentication.helpers.token.config import ACCESS_TOKEN_EXPIRATION, REFRESH_TOKEN_EXPIRATION
from helpers.jwt import JWTHelper
from utils.api.exception import APIException, UnauthorizedException


class TokenBase:
    def __init__(self, token_exp: timedelta, token_type: str | None = None, api_code: int = 0) -> None:
        self.token_exp = token_exp
        self.token_type = token_type
        self.api_code = api_code

    def render(self, user_id: int):
        jwt_helper = JWTHelper(payload={
            'user_id': user_id,
            'type': self.token_type,
            'exp': timezone.now() + self.token_exp
        })

        if jwt_helper.error is not None:
            raise APIException(api_code=self.api_code, error_code=10, error_detail=jwt_helper.error)

        return jwt_helper.token

    def auth(self, token: str) -> int | None:
        jwt_helper = JWTHelper(token=token)

        if jwt_helper.error is not None:
            raise UnauthorizedException(api_code=self.api_code, error_code=10, error_detail=jwt_helper.error)

        if jwt_helper.payload.get('type', None) != self.token_type:
            raise UnauthorizedException(api_code=self.api_code, error_code=11, error_detail='Token type mismatch')

        return jwt_helper.payload.get('user_id', None)


class AccessTokenHelper(TokenBase):
    def __init__(self, api_code: int = 0) -> None:
        super().__init__(ACCESS_TOKEN_EXPIRATION, 'access_token', api_code)


class RefreshTokenHelper(TokenBase):
    def __init__(self, api_code: int = 0) -> None:
        super().__init__(REFRESH_TOKEN_EXPIRATION, 'refresh_token', api_code)
