from typing import Any

from django.contrib.auth import get_user_model

from apps.authentication.constants.api.api_code import APICode
from utils.api.exception import BadRequestException

User = get_user_model()


def register(email, password) -> dict[str, Any]:
    if not isinstance(email, str) or not isinstance(password, str) or not email or not password:
        raise BadRequestException(api_code=APICode.REGISTER, error_detail='Email or password not allowed')

    if User.objects.filter(email=email).exists():
        raise BadRequestException(api_code=APICode.REGISTER, error_detail='User already registered')

    user = User.objects.create_user(email=email, password=password)  # type: ignore

    return user.dict()
