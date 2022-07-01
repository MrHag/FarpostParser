import datetime
from typing import overload
from text_writer import text_writer

class text_dateformat_writer(text_writer):
    def open(self, path: str):
        text_writer.open(self, path)

        tim = datetime.datetime.today()
        strtime = tim.strftime("%d.%m.%Y %H_%M_%S")
        self._open(path, tim, strtime)
    
    def _open(self, path: str, today: datetime.datetime, strtime: str):
        raise NotImplementedError()
