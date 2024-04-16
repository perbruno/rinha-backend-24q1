import psycopg2
from psycopg2.extensions import connection, cursor
import psycopg2.pool

from services.logging import logging
import os

logging.basicConfig(level=logging.DEBUG)


class PSQL:
    _instance = None
    busy = 0

    def __new__(cls):
        if cls._instance is None:
            print("new instance being created")
            cls._instance = super().__new__(cls)
            cls.pool = psycopg2.pool.SimpleConnectionPool(
                1, 50, dsn=os.getenv("DB_HOSTNAME")
            )
        return cls._instance

    def execute(self, action, *args, **kwargs):
        try:
            func = getattr(self, action)
            conn: connection = self.pool.getconn()
            with conn.cursor() as curs:
                ans = func(curs, *args, **kwargs)
            conn.commit() if action == "upsert" else None
            return ans
        except NameError as nerr:
            logging.error(nerr)
            raise
        except BaseException as err:
            logging.error(err)
            raise
        finally:
            self.pool.putconn(conn)

    def upsert(self, curs: cursor, query: str, values: tuple):
        curs.execute(query, values)
        return True

    def select_one(self, curs: cursor, query: str, values: tuple):
        curs.execute(query, values)
        return curs.fetchone()

    def select_many(self, curs: cursor, query: str, values: tuple, limit: int):
        curs.execute(query, values)
        return curs.fetchmany(limit)

    def select_all(self, curs: cursor, query: str, values: tuple):
        curs.execute(query, values)
        return curs.fetchall()


db = PSQL()
