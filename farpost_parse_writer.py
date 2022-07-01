import datetime
from typing import Any, List
from openpyxl import Workbook
import xlsxwriter
from parse_writer import parse_writer


class farpost_parse_writer(parse_writer):
    __workbook: Workbook
    __worksheet: Any
    __row: int
    
    def __init__(self, path: str):
        parse_writer.__init__(self, path)
        self.__row = 0

    def _open(self, path: str, today: datetime.datetime, strtime: str):
        parse_writer._open(self, path, today, strtime)
        self.__workbook = xlsxwriter.Workbook(f'{path}/{strtime}.xlsx')
        self.__worksheet = self.__workbook.add_worksheet()

    def close(self):
        parse_writer.close(self)
        self.__workbook.close()

    def write(self, text: List[str], exceltext: List[str]):
        print("Write......")
        parse_writer.write(self, f'{"; ".join(text)}\n')

        for col, row_text in enumerate(exceltext):
            self.__worksheet.write(self.__row, col, row_text)
        self.__row += 1