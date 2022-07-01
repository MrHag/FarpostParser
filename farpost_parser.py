import re
from typing import Dict, List
import requests
from browser import browser
from captcha_solver import SolveError
from farpost_captcha_solver import captcha_type, farpost_captcha_solver
from farpost_offer import farpost_offer
from farpost_parser_query import farpost_parser_query
from farpost_user import farpost_user
from exiter import exiter
from parser import ParseError, parser, parser_error_handler
from request_master import request_master


class farpost_parser_error_handler(parser_error_handler):
    __solver: farpost_captcha_solver
    __req_master: request_master

    def __init__(self, browser: browser, req_master: request_master, api_key: str):
        self.__solver = farpost_captcha_solver(browser, req_master, api_key)
        self.__req_master = req_master

    def handle(self, req: requests.Request, resp: requests.Response) -> requests.Response:
        code = resp.status_code

        req_master = self.__req_master



        print(f"Code: {code}")

        if code == 403 and len(resp.text) != 0:
            while True:
                try:
                    content = self.__solver.solve(req, captcha_type.PHONE)
                    if content is not None:
                        resp = requests.Response()
                        resp._content = bytes(content, encoding="utf-8")
                        return resp
                    return req_master.req(req, self)
                except SolveError:
                    pass

        if code == 504:
            return req_master.req(req, self)

        #if len(resp.history) > 0 and "verify" in resp.url:
        if req.method != "DELETE" and "verify" in resp.url:
            print("Captcha... ")
            req_master.refresh_session()
            req_master.req(requests.Request("GET", "https://www.farpost.ru/set/sentinel"), self)
            respn = req_master.req(requests.Request("DELETE", "https://www.farpost.ru/verify"), self)
            res = "true" in respn.text

            text = "Ok" if res else "Fail"
            print(f"Captcha: {text}")

            if not res:
                while True:
                    try:
                        content = self.__solver.solve(req, captcha_type.DEFAULT)
                        if content is not None:
                            resp = requests.Response()
                            resp._content = bytes(content, encoding="utf-8")
                            return resp
                        return req_master.req(req, self)
                    except SolveError:
                        pass
            else:
                req_master.req(req, self)

        return resp

class farpost_parser(parser):

    __products: Dict[int, farpost_offer]

    def parse_products(self, exit: exiter = None) -> List[int]:

        query_generator = farpost_parser_query(self._options)

        self.__products = {}

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
                products.extend(farpost_parser.extract_products(resp.text))
            except Exception:
                raise ParseError(req, resp)

            self.__products.update({prod.id: prod for prod in products})

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
            products.append(farpost_offer(id, views, 0, ""))

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
            
            prod = self.__products[id]
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

        # offer = self._database.take_object(farpost_offer, f"\"user_id\" = \"{id}\"")

        # phone = ""

        # if offer is not None:
        phone = self.parse_phone(str(offer_id))

        user = farpost_user(0, id, offers, phone, False)

        try:
            user.products.append(self.__products[offer_id])
        except Exception:
            pass

        user.products.extend(farpost_parser.extract_products(resp.text))

        return user
