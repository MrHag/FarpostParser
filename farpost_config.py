import json
from typing import Any, List

from config import InvalidConfigException, config


class farpost_config(config):

    pages_count: int
    max_views: int
    max_offers: int
    cities: List[str]
    categories: List[str]
    max_price: int
    min_price: int
    price_step: int
    api_key: str

    def _default_config(self) -> dict[str, Any]:
        return {'pages': '5', 'max_views': '100', 'max_offers': '5', 'cities': [
            "moskovskaya-obl", "belgorodskaya-obl"], 'categories': ['zapchasti', "clothes"], 'max_price': '20000', 'min_price': '1000', 'price_step': '2000', 'api_key': 'key'}

    def _cast_and_write(self, conf):
        try:
            self.pages_count = int(conf['pages'])

            self.max_views = int(conf['max_views'])

            self.max_offers = int(conf['max_offers'])

            self.cities = list(conf['cities'])


            self.categories = list(conf['categories'])

            # is_used = conf['is_used'].lower() in 'true'

            self.max_price = int(conf['max_price'])

            self.min_price = int(conf['min_price'])

            self.price_step = int(conf['price_step'])

            self.api_key = conf['api_key']
        except Exception:
            raise InvalidConfigException
