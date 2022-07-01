from sqlite3 import Connection, Cursor
import sqlite3
from typing import Any, List, Tuple, Type, TypeVar

from base_db_entity import base_db_entity


class db:
    __db: Connection
    __filename: str

    T = TypeVar('T', bound=base_db_entity)

    def __init__(self, filename: str, sqls: List[str]):
        self.__filename = filename
        self.__db = sqlite3.connect(self.__filename, check_same_thread=False)
        self.__check_and_create(sqls)

    def __check_and_create(self, sqls: List[str]):
        cur = self.__db.cursor()
        db = self.__db

        for sql in sqls:
            cur.execute(sql)

        db.commit()

    def execute(self, sql: str) -> Cursor:
        return self.__db.cursor().execute(sql)

    def confirm(self):
        self.__db.commit()

    def save_object(self, entity: T):
        pack = entity.pack()

        q = '"'
        table_name = type(entity).table_name
        table_columns = ','.join(pack.keys())
        values = ','.join([f'{q}{p}{q}' for p in pack.values()])

        sql = f"INSERT INTO {table_name}({table_columns}) VALUES ({values})"

        # print(f"SQL: {sql}")

        cur = self.__db.cursor()
        cur.execute(sql)
        self.confirm()

        # print(f"ROW: {cur.lastrowid}")

        return cur.lastrowid

    def update_object(self, before_entity: T, after_entity: T, sql_conditions: str):
        before_pack = before_entity.pack()
        after_pack = after_entity.pack()

        for key, value in after_pack.items()[:]:
            if(before_pack[key] != value):
                del[after_pack[key]]

        q = '"'
        table_name = type(after_entity).table_name
        pairs_key_value = ['='.join([key, f'{q}{value}{q}'])
                           for key, value in after_pack.items()]
        columns_value = ','.join(pairs_key_value)

        sql = f"UPDATE {table_name} SET {columns_value} WHERE {sql_conditions}"

        self.__db.cursor().execute(sql)
        self.confirm()

    def take_objects(self, entity_type: Type[T], sql_conditions: str) -> List[T]:

        sql = f"SELECT * FROM {entity_type.table_name} WHERE {sql_conditions}"
        cur = self.__db.cursor()

        cur.execute(sql)
        fetch = cur.fetchall()

        objects = []

        for entity in fetch:
            objects.append(entity_type.from_pack_list(entity))

        return objects

    def take_object(self, entity_type: Type[T], sql_conditions: str) -> T | None:

        sql = f"SELECT * FROM {entity_type.table_name} WHERE {sql_conditions}"

        cur = self.__db.cursor()

        cur.execute(sql)

        entity: Tuple[Any, Any]
        entity = cur.fetchone()

        if entity is None:
            return None

        object = entity_type.from_pack_list(entity)

        return object

    def object_exists(self, entity_type: Type[T], id: Any = None, sql_conditions: str = None) -> bool:

        conditions = []

        if id is not None:
            conditions.append(f"id = \"{id}\"")

        if sql_conditions is not None:
            conditions.append(sql_conditions)

        cond = ' AND '.join(conditions)

        sql = f"SELECT EXISTS (SELECT 1 FROM {entity_type.table_name} WHERE {cond})"

        #print(f"SQL: {sql}")

        cur = self.__db.cursor()

        cur.execute(sql)

        entity: Tuple[int, Any]

        entity = cur.fetchone()

        return bool(entity[0])
