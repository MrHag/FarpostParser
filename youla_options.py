from typing import List
from typing_extensions import Self

from options import options
from youla_config import youla_config


class youla_options(options):
    pages_count: int
    cities: List[str]
    categories: List[str]
    max_price: int
    min_price: int

    def from_cfg(cfg: youla_config) -> Self:
        options = youla_options()
        options.pages_count = cfg.pages_count
        options.categories = cfg.categories
        options.cities = cfg.cities
        options.max_price = cfg.max_price
        options.min_price = cfg.min_price
        return options