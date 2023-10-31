from django.http import HttpRequest
from django.middleware import csrf


def get_csrf_token(request: HttpRequest):
    return {'csrfmiddlewaretoken': csrf.get_token(request)}
