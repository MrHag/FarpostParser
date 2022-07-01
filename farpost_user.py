from typing import Any, Dict, List
from typing_extensions import Self
from farpost_offer import farpost_offer

from user import user


class farpost_user(user):
    offers_count: int
    phone: str

    products: List[farpost_offer]

    def __init__(self, id: int, user_id: str, offers_count: int, phone: str, is_scammed: bool):
        super().__init__(id, user_id, is_scammed)
        self.offers_count = offers_count
        self.phone = phone
        self.products = []

    @classmethod
    def from_pack(cls, pack: Dict[str, Any]) -> Self:
        user = cls(int(pack['id']), pack['user_id'], int(pack['offers_count']), pack['phone'], bool(pack['is_scammed']))
        return user

    @classmethod
    def from_pack_list(cls, pl: List[Any]) -> Self:
        user = cls(int(pl[0]), pl[1], int(pl[2]), pl[3], bool(pl[4]))
        return user

    def pack(self) -> Dict[str, str]:
        return dict(user_id=self.user_id, offers_count=str(self.offers_count), phone=self.phone, is_scammed=str(int(self.is_scammed)))
        