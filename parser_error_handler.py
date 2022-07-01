import requests


class parser_error_handler:
    def handle(self, req: requests.Request, resp: requests.Response) -> requests.Response:
        raise NotImplementedError()
