from typing import List, TypeVar
from typing_extensions import Self

from config import config


class options:

    T = TypeVar('T', bound=config)

    def from_cfg(cfg: T) -> Self:
        pass
