import json
from datetime import date, datetime
from typing import Any, Generator

from django.db.models import QuerySet


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        if isinstance(o, QuerySet):
            return list(o.values())

        if isinstance(o, Generator):
            return list(o)

        try:
            return super().default(o)
        except Exception:
            return str(o)


class JsonHelper:
    @staticmethod
    def encode(obj):
        return MyEncoder().encode(obj)

    @staticmethod
    def decode(s: str | bytes | bytearray) -> dict[str, Any]:
        return json.loads(s)
