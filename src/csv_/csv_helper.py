import codecs
import csv
from typing import Iterable

from django.http import HttpResponse


class CSVHelper:
    def __init__(self, file_name: str):
        self.response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{file_name}"'},
        )
        self.__writer = None

    def __get_writer(self):
        if self.__writer is None:
            self.__writer = csv.writer(self.response)
        return self.__writer

    def write_row(self, row: Iterable):
        self.__get_writer().writerow(row)

    def use_bom_utf8(self):
        self.response.write(codecs.BOM_UTF8)
        return self
