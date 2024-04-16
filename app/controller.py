from model import (
    is_client,
    limit_exceeded,
    insert_transaction,
    select_balance,
    select_transactions,
    update_balance,
)
from functools import wraps


def check_client(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not bool(is_client(kwargs.get("client_id"))):
            raise IndexError("cliente invalido")

        return func(*args, **kwargs)

    return inner


def check_limit(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if limit_exceeded(kwargs.get("client_id"), kwargs.get("amount")):
            raise ValueError("This transaction will surpass the client limit")
        return func(*args, **kwargs)

    return inner


def credit_amount(client_id, amount, description):
    insert_transaction("credit", client_id, amount, description)


@check_limit
def debit_amount(client_id, amount, description):
    insert_transaction("debit", client_id, amount, description)


def get_balance(client_id):
    balance, limit = select_balance(client_id)
    return {
        "limit": limit,
        "balance": balance,
    }
    pass


def get_last_transactions(client_id):
    transactions = select_transactions(client_id)

    format = lambda dt: dict(
        zip(("type", "amount", "description", "timestamp"), dt[2:])
    )
    return list(map(format, transactions))


@check_client
def get_client_statement(client_id):
    return dict(
        balance=get_balance(client_id),
        last_transactions=get_last_transactions(client_id),
    )


@check_client
def create_client_transaction(transaction_type, amount, description, client_id):
    if transaction_type == "c":
        credit_amount(client_id=client_id, amount=amount, description=description)
    else:
        debit_amount(client_id=client_id, amount=amount, description=description)
        amount *= -1
    update_balance(client_id, amount)
    return get_balance(client_id)
