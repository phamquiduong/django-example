from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.authentication.constants.api.api_code import APICode
from utils.api.exception import BadRequestException, ConflictException

User = get_user_model()


def register(email, password) -> dict[str, Any]:
    if not isinstance(email, str) or not email:
        raise BadRequestException(api_code=APICode.REGISTER, error_code=100, error_detail='Email is not valid',
                                  error_fields={'email': 'Email is multiple, null or empty'})

    if not isinstance(password, str) or not password:
        raise BadRequestException(api_code=APICode.REGISTER, error_code=110, error_detail='Password is not valid',
                                  error_fields={'password': 'Password is multiple, null or empty'})

    try:
        validate_password(password=password)
    except ValidationError as exc:
        raise BadRequestException(api_code=APICode.REGISTER, error_code=111, error_detail='Password is not valid',
                                  error_fields={'password': exc.messages}) from exc

    if User.objects.filter(email=email).exists():
        raise ConflictException(api_code=APICode.REGISTER, error_code=100, error_detail='User already registered')

    user = User.objects.create_user(email=email, password=password)  # type: ignore

    return user.dict()
