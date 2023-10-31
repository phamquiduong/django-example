from typing import Any

from django.contrib.auth import get_user_model

from apps.authentication.constants.api.api_code import APICode
from utils.api.exception import BadRequestException

User = get_user_model()


def register(email, password) -> dict[str, Any]:
    if not isinstance(email, str) or not email:
        raise BadRequestException(api_code=APICode.REGISTER, error_code=101, error_detail='Email is not valid',
                                  error_fields={'email': 'Email is multiple, null or empty'})

    if not isinstance(password, str) or not password:
        raise BadRequestException(api_code=APICode.REGISTER, error_code=111, error_detail='Password is not valid',
                                  error_fields={'password': 'Password is multiple, null or empty'})

    if User.objects.filter(email=email).exists():
        raise BadRequestException(api_code=APICode.REGISTER, error_code=102, error_detail='User already registered',
                                  error_fields={'email': 'Email already exists'})

    user = User.objects.create_user(email=email, password=password)  # type: ignore

    return user.dict()
