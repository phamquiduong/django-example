from typing import Any

import jwt

from helpers.jwt.config import ALGORITHM, SECRET_KEY, Message


class JWTHelper:
    def __init__(self, token: str | None = None, payload: dict[str, Any] | None = None) -> None:
        if (token is None and payload is None) or (token is not None and payload is not None):
            raise AttributeError('You must provide only a token or payload')

        self.error = None

        if token is not None:
            self.__set_token(token=token)

        if payload is not None:
            self.__set_payload(payload=payload)

    def __set_payload(self, payload: dict[str, Any]):
        self.payload = payload

        try:
            self.token = jwt.encode(
                payload=payload,
                key=SECRET_KEY,
                algorithm=ALGORITHM)
        except Exception as ex:
            self.error = str(ex)

        return self

    def __set_token(self, token: str):
        self.token = token

        try:
            self.payload = jwt.decode(
                jwt=token,
                key=SECRET_KEY,
                algorithm=ALGORITHM)
        except jwt.ExpiredSignatureError:
            self.error = Message.EXPIRED_SIGNATURE_ERROR
        except jwt.InvalidTokenError:
            self.error = Message.INVALID_TOKEN_ERROR
        except Exception as ex:
            self.error = str(ex)

        return self
