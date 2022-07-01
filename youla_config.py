import json
from typing import Any, List

from config import InvalidConfigException, config


class youla_config(config):

    pages_count: int
    max_views: int
    max_active_offers: int
    max_sold_offers: int
    cities: List[str]
    categories: List[str]
    max_price: int
    min_price: int

    def _default_config(self) -> dict[str, Any]:
        return {'pages': '5', 'max_views': '100', 'max_active_offers': '5', 'max_sold_offers': '5', 'cities': [
            "576d0612d53f3d80945f8b5d", "576d0612d53f3d80945f8b5e"], 'categories': ['avto-moto', "zhenskaya-odezhda"], 'max_price': '20000', 'min_price': '1000'}

    def _cast_and_write(self, conf):
        try:
            self.pages_count = int(conf['pages'])

            self.max_views = int(conf['max_views'])

            self.max_active_offers = int(conf['max_active_offers'])

            self.max_sold_offers = int(conf['max_sold_offers'])

            self.cities = list(conf['cities'])


            self.categories = list(conf['categories'])

            # is_used = conf['is_used'].lower() in 'true'

            self.max_price = int(conf['max_price'])

            self.min_price = int(conf['min_price'])

        except Exception:
            raise InvalidConfigException
