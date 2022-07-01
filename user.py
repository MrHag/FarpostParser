from typing import Any, Dict, List
from typing_extensions import Self
from base_db_entity import base_db_entity


class user(base_db_entity):
    id: int
    user_id: str
    is_scammed: bool

    table_name = "users"

    def __init__(self, id: str, user_id: str, is_scammed: bool):
        self.id = id
        self.user_id = user_id
        self.is_scammed = is_scammed