from enum import StrEnum

from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'


class Message(StrEnum):
    EXPIRED_SIGNATURE_ERROR = 'Signature expired'
    INVALID_TOKEN_ERROR = 'Invalid token'
