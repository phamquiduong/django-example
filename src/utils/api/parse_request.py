from django.http import HttpRequest

from helpers.json import JsonHelper


def parse_request(request: HttpRequest):
    try:
        return JsonHelper.decode(request.body)
    except Exception:
        if request.method == 'GET':
            return request.GET.dict()
        return request.POST.dict()
