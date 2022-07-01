from typing import List, TypeVar
import requests
from db import db
from offer import offer
from options import options
from parser_error_handler import parser_error_handler
from user import user
from exiter import exiter
from request_master import request_master


class ParseError(Exception):
    req: requests.Request
    resp: requests.Response

    def __init__(self, request: requests.Request, responce: requests.Response):
        super().__init__()
        self.req = request
        self.resp = responce
    """Raised when the parse is fail"""
    pass


class parser:

    TO = TypeVar('TO', bound=options)

    _options: TO
    _request_master: request_master
    _error_handler: parser_error_handler
    _database: db

    def __init__(self, parser_options: TO, request_master: request_master, error_handler: parser_error_handler, database: db):
        self._options = parser_options
        self._request_master = request_master
        self._error_handler = error_handler
        self._database = database

    def parse_products(self, exit: exiter = None) -> List[int]:
        raise NotImplementedError()

    T = TypeVar('T', bound=offer)

    def parse_product(self, id: str) -> T:
        raise NotImplementedError()

    T2 = TypeVar('T2', bound=user)

    def parse_user(self, id: str, offer_id: int) -> T2:
        raise NotImplementedError()