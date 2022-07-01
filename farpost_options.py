from typing import List
from typing_extensions import Self
from farpost_config import farpost_config

from options import options


class farpost_options(options):
    pages_count: int
    cities: List[str]
    categories: List[str]
    max_price: int
    min_price: int
    price_step: int
    api_key: str

    def from_cfg(cfg: farpost_config) -> Self:
        options = farpost_options()
        options.pages_count = cfg.pages_count
        options.categories = cfg.categories
        options.cities = cfg.cities
        options.max_price = cfg.max_price
        options.min_price = cfg.min_price
        options.price_step = cfg.price_step
        options.api_key = cfg.api_key
        return options