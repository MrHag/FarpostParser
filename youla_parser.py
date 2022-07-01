import json
from typing import List
import time

import requests
from youla_options import youla_options
from browser import browser
from captcha_solver import SolveError, captcha_solver
from exiter import exiter
from youla_offer import youla_offer
from parser import ParseError, parser, parser_error_handler

from youla_parser_query import youla_parser_query
from request_master import request_master
from youla_user import youla_user


class youla_parser_error_handler(parser_error_handler):
    __solver: captcha_solver

    def __init__(self, browser: browser):
        self.__solver = captcha_solver(browser)

    def handle(self, resp: requests.Response):

        return
        html = resp.text
        pattern = ""

        while True:
            try:
                self.__solver.solve()
                return
            except SolveError:
                pass


class youla_parser(parser):

    def parse_products(self, exit: exiter = None) -> List[str]:

        offers_id: List[str] = []

        query_generator = youla_parser_query(self._options)

        while exit is None or not exit.is_exit():

            if exit is not None:
                exit.pause()

            req = query_generator.next()
            if req == None:
                break
            resp = self._request_master.req(req)

            if resp.status_code != 200:
                self._error_handler.handle(resp)
                continue
            
            try:
                json = resp.json()
                data = json["data"]
                items = data["feed"]["items"]
            except Exception:
                raise ParseError(req, resp)

            for item in items:
                try:
                    product_id = item["product"]["id"]
                    offers_id.append(product_id)
                except Exception:
                    pass

        return offers_id

    def parse_product(self, id: str) -> youla_offer | None:

        req = youla_parser_query.product_query(id)
        resp = self._request_master.req(req)

        if resp.status_code != 200:
            self._error_handler.handle(resp)
            return None

        try:
            json = resp.json()
            data = json["data"]
            id = data["id"]
            views = int(data["views"])
            price = int(data["price"])/100
            user_id = data["owner"]["id"]
        except Exception:
                raise ParseError(req, resp)

        off = youla_offer(id, views, price, user_id)
        return off

    def parse_user(self, id: str) -> youla_user | None:

        req = youla_parser_query.user_query(id)
        resp = self._request_master.req(req)

        if resp.status_code != 200:
            self._error_handler.handle(resp)
            return None

        try:
            json = resp.json()
            data = json["data"]

            active_offers_count = int(data["prods_active_cnt"])
            sold_offers_count = int(data["prods_sold_cnt"])
            is_store = data["store"] is not None
        except Exception:
                raise ParseError(req, resp)

        usr = youla_user(id, active_offers_count,
                   sold_offers_count, is_store, False)
        return usr
