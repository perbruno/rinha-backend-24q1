from infra.postgresql import db
import constants as const
from os import path, getcwd
from services.logging import logging

logging.basicConfig(level=logging.DEBUG)


def get_sql_file(name):
    with open(path.join(getcwd(), const.QUERIES, f"{name}.sql"), "r") as fl:
        return fl.read()


def is_client(id) -> bool:
    (result,) = db.execute("select_one", get_sql_file("select_client"), (id,))
    return result


def select_balance(id):
    balance, limit = db.execute("select_one", get_sql_file("select_balance"), (id,))
    return balance, limit


def limit_exceeded(id, amount) -> bool:
    balance, limit = select_balance(id)
    return balance - amount < -limit


def select_transactions(id, limit=10):
    transactions = db.execute(
        "select_many",
        get_sql_file("select_transactions"),
        dict(id=id, limit=limit),
        limit,
    )
    return transactions


def insert_transaction(transaction_type, client_id, amount, description):
    db.execute(
        "upsert",
        get_sql_file("insert_transactions"),
        dict(
            client_id=client_id,
            amount=amount,
            description=description,
            category=transaction_type,
        ),
    )


def update_balance(client_id, amount):
    db.execute(
        "upsert",
        get_sql_file("update_balance"),
        dict(client_id=client_id, amount=amount),
    )
