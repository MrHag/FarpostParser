from typing import Any, Dict, List
from typing_extensions import Self
from base_db_entity import base_db_entity


class offer(base_db_entity):
    id: int
    user_id: int
    inner_user_id: str
    table_name = "offers"

    def __init__(self, id: int, user_id: int, user_inner_id: str):
        self.id = id
        self.user_id = user_id
        self.user_inner_id = user_inner_id
