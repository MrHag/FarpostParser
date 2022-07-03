from core import core
from farpost_config import farpost_config
from farpost_options import farpost_options
from farpost_config import farpost_config
from farpost_offer import farpost_offer
from farpost_options import farpost_options
from farpost_parse_writer import farpost_parse_writer
from farpost_parser import farpost_parser
from farpost_parser_error_handler import farpost_parser_error_handler
from farpost_user import farpost_user


class farpost_core(core):

    config_type = farpost_config
    options_type = farpost_options
    user_type = farpost_user
    offer_type = farpost_offer
    parser_type = farpost_parser

    SQL = ['CREATE TABLE IF NOT EXISTS users(id integer primary key autoincrement, user_id text unique, offers_count integer, phone text, is_scammed integer)',
           'CREATE TABLE IF NOT EXISTS offers(id integer primary key, views integer, user_id integer, foreign key (user_id) references users (id))']

    RESSQL = [
        'CREATE TABLE IF NOT EXISTS offers(id integer primary key, views integer, user_id integer)']

    cfg: config_type
    opt: options_type

    p_writer: farpost_parse_writer

    def start(self):
        self.p_writer = farpost_parse_writer("parsed/")
        try:
            core.start(self)
        finally:
            self.p_writer.close()

    def user_is_approp(self, usr: farpost_user):
        cfg = self.cfg
        return usr.offers_count <= cfg.max_offers and usr.phone != ""

    def write_out(self, usr: farpost_user, offer: farpost_offer):

        prod = min(usr.products, key=lambda prod: prod.views)

        self.p_writer.write([f"https://www.farpost.ru/{prod.id}", f"https://api.whatsapp.com/send?phone={usr.phone}"],
                            [usr.phone, f"https://www.farpost.ru/{prod.id}"])

    def offer_is_approp(self, prod: farpost_offer):
        cfg = self.cfg
        return prod.views <= cfg.max_views

    def init_error_handler(self) -> farpost_parser_error_handler:
        return farpost_parser_error_handler(self.brw, self.req_master, self.opt.api_key)
