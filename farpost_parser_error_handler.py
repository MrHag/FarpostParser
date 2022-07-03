import requests
from browser import browser
from captcha_solver import SolveError
from farpost_captcha_solver import captcha_type, farpost_captcha_solver
from parser import parser_error_handler
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

        # if len(resp.history) > 0 and "verify" in resp.url:
        if req.method != "DELETE" and "verify" in resp.url:
            print("Captcha... ")
            req_master.refresh_session()
            req_master.req(requests.Request(
                "GET", "https://www.farpost.ru/set/sentinel"), self)
            respn = req_master.req(requests.Request(
                "DELETE", "https://www.farpost.ru/verify"), self)
            res = "true" in respn.text

            text = "Ok" if res else "Fail"
            print(f"Captcha: {text}")

            if not res:
                while True:
                    try:
                        content = self.__solver.solve(
                            req, captcha_type.DEFAULT)
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
