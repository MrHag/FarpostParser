from typing import Any, Dict, List
from typing_extensions import Self
from base_db_entity import base_db_entity
from offer import offer


class youla_offer(offer):
    views: int
    price: int

    def __init__(self, id: str, views: int, price: int, user_id: str):
        super().__init__(id, user_id)
        self.views = views
        self.price = price

    @classmethod
    def from_pack(cls, pack: Dict[str, Any]) -> Self:
        offer = cls(pack['id'], int(pack['views']), int(pack['price']), pack['user_id'])
        return offer

    @classmethod
    def from_pack_list(cls, pl: List[Any]) -> Self:
        offer = cls(pl[0], int(pl[1]), int(pl[2]), pl[3])
        return offer

    def pack(self) -> Dict[str, str]:
        return dict(id=self.id, views=str(self.views), price=str(self.price), user_id=self.user_id)
