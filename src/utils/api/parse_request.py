from typing import Any

from django.http import HttpRequest

from helpers.json import JsonHelper


def parse_request(request: HttpRequest) -> dict[str, Any]:
    try:
        return JsonHelper.decode(request.body)
    except Exception:
        if request.method == 'GET':
            return request.GET.dict()
        return request.POST.dict()
