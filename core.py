import json
from typing import TypeVar
from browser import browser
from db import db
from exiter import exiter
from options import options
from parser import ParseError, parser_error_handler
from request_master import request_master
from config import config
from offer import offer
from parser import parser
from user import user

class core:

    config_type = config
    options_type = options
    user_type = user
    offer_type = offer
    parser_type = parser

    SQL = []

    database: db
    cfg: config_type
    brw: browser
    req_master: request_master
    opt: options_type
    pars: parser_type

    def __init__(self, database: db, cfg: config_type, brw: browser, req_master: request_master):
        self.database = database
        self.cfg = cfg
        self.brw = brw
        self.req_master = req_master
        self.opt = self.options_type.from_cfg(cfg)

        error_handler = self.init_error_handler()

        self.pars = self.parser_type(
            self.opt, req_master, error_handler, self.database)

    def user_is_approp(self, usr: user_type):
        raise NotImplementedError()

    def write_out(self, usr: user_type, offer: offer_type):
        raise NotImplementedError()

    def offer_is_approp(self, prod: offer_type):
        raise NotImplementedError()

    def init_error_handler(self) -> parser_error_handler:
        raise NotImplementedError()

    def start(self):
        database = self.database
        cfg = self.cfg

        cls = type(self)

        exit = exiter(cfg.exit_hotkey, cfg.pause_hotkey)

        prse = self.pars

        ot = cls.offer_type

        ou = cls.user_type

        TO = TypeVar('TO', bound=ot)
        TU = TypeVar('TU', bound=ou)

        def accept_offer(prod: TO, usr: TU) -> TU:
            if usr is not None:
                return usr

            usr = prse.parse_user(prod.inner_user_id, prod.id)

            if usr is None:
                return None

            if self.user_is_approp(usr):
                usr.is_scammed = True
                self.write_out(usr, prod)

            usr.id = database.save_object(usr)

            return usr

        products = prse.parse_products(exit)
        exit.reset()

        for i, prod_id in enumerate(products):

            try:

                if exit.is_exit():
                    print("Exiting...")
                    break
                exit.pause()

                print(f"\nFilter {i+1} of {len(products)}")

                if database.object_exists(cls.offer_type, prod_id):
                    continue

                prod: TO

                prod = prse.parse_product(prod_id)

                if prod is None:
                    continue

                usr = database.take_object(
                    cls.user_type, f"\"user_id\" = \"{prod.inner_user_id}\"")

                if usr is not None:
                    prod.user_id = usr.id

                if self.offer_is_approp(prod):
                    usr = accept_offer(prod, usr)

                database.save_object(prod)
            except ParseError as e:
                print("ParseError")
                with open("reqERROR.txt", "w", encoding="utf-8") as f:
                    f.write(json.dumps(
                        {
                            "cookies": json.dumps(e.req.cookies),
                            "data": json.dumps(e.req.data),
                            "headers": json.dumps(e.req.headers),
                            "json": json.dumps(e.req.json),
                            "method": json.dumps(e.req.method),
                            "url": json.dumps(e.req.url),
                            "params": json.dumps(e.req.params)
                        })
                    )
                with open("respERROR.txt", "w", encoding="utf-8") as f:
                    f.write(e.resp.text)
