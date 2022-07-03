import re
from typing import Callable, Dict, List, TypeVar
from db import db
from farpost_offer import farpost_offer
from farpost_parser_query import farpost_parser_query
from farpost_user import farpost_user
from exiter import exiter
from options import options
from parser import ParseError, parser
from parser_error_handler import parser_error_handler
from request_master import request_master


class farpost_parser(parser):

    products: Dict[int, farpost_offer]

    TO = TypeVar('TO', bound=options)

    def __init__(self, parser_options: TO, request_master: request_master, error_handler: parser_error_handler, database: db):
        super().__init__(parser_options, request_master, error_handler, database)
        self.products = {}

    def parse_products(self, map: Callable[[farpost_offer], None], exit: exiter = None) -> List[int]:

        query_generator = farpost_parser_query(self._options)

        self.products = {}

        products: List[farpost_offer]
        products = []

        while exit is None or not exit.is_exit():

            if exit is not None:
                exit.pause()

            req = query_generator.next()
            if req == None:
                break

            resp = self._request_master.req(req, self._error_handler)

            try:
                prods = farpost_parser.extract_products(resp.text)

                [map(prod) for prod in prods]

                products.extend(prods)
            except Exception:
                raise ParseError(req, resp)

            self.products.update({prod.id: prod for prod in products})

        return [prod.id for prod in products]

    def extract_products(text: str) -> List[farpost_offer]:
        products = []

        groups = re.findall(r'<a  name=\\\"[0-9].*?a>', text)

        for prod in groups:
            id = re.search(r'(?<=name=\\\")[0-9]+(?=\\\")', prod)
            views = re.search(r'(?<=data-stat=\\\")[0-9]+(?=\\\")', prod)
            if id is None or views is None:
                continue
            id = int(id[0])
            views = int(views[0])
            #print("Id: ", id)
            products.append(farpost_offer(id, views, 0))

        return products

    def parse_product(self, id: str) -> farpost_offer | None:

        req = farpost_parser_query.product_query(id)
        resp = self._request_master.req(req, self._error_handler)

        try:

            user_link = re.search(
                r'(?<=class="userNick auto-shy ">).*?(?=</s)', resp.text, re.S)

            if user_link is None:
                return None

            user_address = re.search(
                r'(?<=<a href="/).*?(?=")', user_link[0], re.S)[0]
            userid = user_address.split('/')[1]

            prod = self.products[id]
            prod.inner_user_id = userid

        except Exception:
            raise ParseError(req, resp)

        return prod

    def parse_phone(self, prod_id: str) -> str:
        req = farpost_parser_query.phone_query(prod_id)
        resp = self._request_master.req(req, self._error_handler)

        print("PARSE PHONE")
        phone = re.search(r'\+([0-9 -][()]?){15,}', resp.text)
        if phone is None:
            print("PHONE ERROR")
            with open("PHONEERROR.txt", "w", encoding="utf-8") as f:
                f.write(resp.text)
            return ""
        phone = phone.group(0)
        return re.sub('\D', '', phone)

    def parse_user(self, id: str, offer_id: int) -> farpost_user | None:
        req = farpost_parser_query.user_query(id)
        resp = self._request_master.req(req, self._error_handler)

        try:
            offers = re.search(r'(?<=data-count=\")[0-9]+', resp.text)
            offers = int(offers[0])
        except Exception:
            raise ParseError(req, resp)

        phone = self.parse_phone(str(offer_id))

        user = farpost_user(0, id, offers, phone, False)

        try:
            user.products.append(self.products[offer_id])
        except Exception:
            pass

        user.products.extend(farpost_parser.extract_products(resp.text))

        return user
