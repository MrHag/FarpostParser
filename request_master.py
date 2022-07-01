import requests
from requests.sessions import Session
from soupsieve import Dict

from parser_error_handler import parser_error_handler


class request_master:
    session: Session

    headers: Dict[str, str]

    def __new_session(self) -> Session:
        session = Session()
        session.headers = self.headers
        #session.verify = False
        return session

    def set_cookies(self, cookies: Dict[str, str]):
        self.session.cookies.clear_session_cookies()
        for key, value in cookies.items():
            self.session.cookies.set(key, value)

    def refresh_session(self):
        self.session = self.__new_session()

    def __init__(self, headers: Dict[str, str]):
        self.headers = headers
        self.refresh_session()

    def req(self, req: requests.Request, error_handler: parser_error_handler) -> requests.Response:
        #  req = requests.Request('GET', 'https://httpbin.org/get')
        preq = self.session.prepare_request(req)
        resp = self.session.send(preq)
        resp = error_handler.handle(req, resp)
        return resp
