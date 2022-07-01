from typing import Any, Dict, List
from typing_extensions import Self

class base_db_entity:
    id: Any
    table_name = ""

    def pack(self) -> Dict[str, str]:
        raise NotImplementedError()

    @classmethod
    def from_pack(cls, pack: Dict[str, Any]) -> Self:
        raise NotImplementedError()

    @classmethod
    def from_pack_list(cls, pl: List[Any]) -> Self:
        raise NotImplementedError()