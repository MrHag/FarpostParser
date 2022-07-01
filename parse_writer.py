import datetime
from io import TextIOWrapper
import os
from typing import Any
from openpyxl import Workbook
import openpyxl

from text_dateformat_writer import text_dateformat_writer


class parse_writer(text_dateformat_writer):

    _file: TextIOWrapper

    def __init__(self, path: str):
        text_dateformat_writer.open(self, path)

    def _open(self, path: str, today: datetime.datetime, strtime: str):
        full_path = f"{path}/{strtime}.txt"
        self._file = open(full_path, "w", encoding="utf-8", buffering=True)

    def close(self):
        self._file.close()

    def write(self, text: str):
        self._file.write(text)
        self._file.flush()

