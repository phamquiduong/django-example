import json
from datetime import date, datetime

from django.db.models import QuerySet


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        if isinstance(o, QuerySet):
            return list(o.values())

        try:
            return super().default(o)
        except Exception:
            return str(o)


class JsonHelper:
    @staticmethod
    def encode(obj):
        return MyEncoder().encode(obj)

    @staticmethod
    def decode(s: str):
        return json.loads(s)
