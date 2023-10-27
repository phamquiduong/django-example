from datetime import timedelta

from django.utils import timezone

from apps.authentication.helpers.token.config import ACCESS_TOKEN_EXPIRATION, REFRESH_TOKEN_EXPIRATION
from constants.api.api_code import APICode
from helpers.jwt import JWTHelper
from utils.api.exception import APIException, UnauthorizedException


class TokenBase:
    def __init__(self, user_id: int, token_exp: timedelta, token_type: str | None = None) -> None:
        self.user_id = user_id
        self.token_exp = token_exp
        self.token_type = token_type

    def render(self):
        jwt_helper = JWTHelper(payload={
            'user_id': self.user_id,
            'type': self.token_type,
            'exp': timezone.now() + self.token_exp
        })

        if jwt_helper.error is not None:
            raise APIException(api_code=APICode.LOGIN, error_detail=jwt_helper.error)

        return jwt_helper.token

    def auth(self, token: str):
        jwt_helper = JWTHelper(token=token)

        if jwt_helper.error is not None:
            raise UnauthorizedException(api_code=APICode.LOGIN, error_detail=jwt_helper.error)

        return True


class AccessTokenHelper(TokenBase):
    def __init__(self, user_id: int) -> None:
        super().__init__(user_id, ACCESS_TOKEN_EXPIRATION, 'access_token')


class RefreshTokenHelper(TokenBase):
    def __init__(self, user_id: int) -> None:
        super().__init__(user_id, REFRESH_TOKEN_EXPIRATION, 'refresh_token')
