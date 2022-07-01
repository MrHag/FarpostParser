import requests
from soupsieve import Any
from browser import browser
from request_master import request_master

class SolveError(Exception):
    """Raised when the solve failed"""
    pass

class captcha_solver:
    brw: browser
    req_master: request_master

    def __init__(self, browser: browser, req_master: request_master) -> str | None:
        self.brw = browser
        self.req_master = req_master

    def solve(self, req: requests.Request, data: Any):
        raise NotImplementedError()