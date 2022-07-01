from typing import Any, Dict, List
from typing_extensions import Self

from user import user


class youla_user(user):
    active_offers_count: int
    sold_offers_count: int
    is_store: bool

    def __init__(self, id: str, active_offers_count: int, sold_offers_count: int, is_store: bool, is_scammed: bool):
        super().__init__(id, is_scammed)
        self.active_offers_count = active_offers_count
        self.sold_offers_count = sold_offers_count
        self.is_store = is_store

    @classmethod
    def from_pack(cls, pack: Dict[str, Any]) -> Self:
        user = cls(pack['id'], int(pack['active_offers_count']), int(pack['sold_offers_count']), bool(pack['is_store']), bool(pack['is_scammed']))
        return user

    @classmethod
    def from_pack_list(cls, pl: List[Any]) -> Self:
        user = cls(pl[0], int(pl[1]), int(pl[2]), bool(pl[3]), bool(pl[4]))
        return user

    def pack(self) -> Dict[str, str]:
        return dict(id=self.id, active_offers_count=str(self.active_offers_count), sold_offers_count=str(self.sold_offers_count), is_store=str(int(self.is_store)), is_scammed=str(int(self.is_scammed)))
        