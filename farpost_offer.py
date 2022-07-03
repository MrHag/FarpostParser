from typing import Any, Dict, List
from typing_extensions import Self
from offer import offer


class farpost_offer(offer):
    views: int

    def __init__(self, id: int, views: int, user_id: int):
        super().__init__(id, user_id, "")
        self.views = views

    @classmethod
    def from_pack(cls, pack: Dict[str, Any]) -> Self:
        offer = cls(int(pack['id']), int(pack['views']), pack['user_id'])
        return offer

    @classmethod
    def from_pack_list(cls, pl: List[Any]) -> Self:
        offer = cls(int(pl[0]), int(pl[1]), pl[2])
        return offer

    def pack(self) -> Dict[str, str]:
        return dict(id=str(self.id), views=str(self.views), user_id=self.user_id)
