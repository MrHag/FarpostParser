import threading
from browser import browser
from core import core
from db import db
from exiter import exiter
from parse_writer import parse_writer
from parser import parser_error_handler
from request_master import request_master
from thread_waiter import thread_waiter
from youla_config import youla_config
from youla_offer import youla_offer
from youla_options import youla_options
from youla_parser import youla_parser, youla_parser_error_handler
from youla_user import youla_user


class youla_core(core):

    config_type = youla_config
    options_type = youla_options
    user_type = youla_user
    offer_type = youla_offer
    parser_type = youla_parser

    error_handler_type = youla_parser_error_handler

    SQL = ['CREATE TABLE IF NOT EXISTS offers(id text primary key, views integer, price integer, user_id integer)',
           'CREATE TABLE IF NOT EXISTS users(id text primary key, user_id text, active_offers_count integer, sold_offers_count integer, is_store integer, is_scammed integer)']

    cfg: config_type

    def user_is_approp(self, usr: youla_user):
        cfg = self.cfg
        return not usr.is_store and usr.active_offers_count <= cfg.max_active_offers and usr.sold_offers_count <= cfg.max_sold_offers

    def write_user(self, usr: youla_user):
        self.p_writer.write(f"https://youla.ru/user/{usr.id}\n")

    def offer_is_approp(self, prod: youla_offer):
        cfg = self.cfg
        return prod.views <= cfg.max_views and (cfg.min_price <= prod.price <= cfg.max_price)
