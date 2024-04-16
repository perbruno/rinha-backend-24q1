from datetime import datetime, UTC
from dataclasses import dataclass, asdict
from enum import StrEnum, auto

from services.logging import logging

logging.basicConfig(level=logging.DEBUG)


class TransactionType(StrEnum):
    c = auto()
    d = auto()


@dataclass(repr=True)
class Transaction:
    valor: int
    tipo: str
    descricao: str

    def _validate_types(self, item: tuple) -> None:
        logging.debug(f"validating {item}")
        parameter, value_type = item

        value = self.__getattribute__(parameter)

        def check_string_len():
            string_len = value.__len__()
            if not (string_len >= 1 and string_len <= 10):
                raise ValueError(f"{parameter} must have one to ten characters")

        if parameter == "tipo" and (value not in TransactionType.__members__):
            raise ValueError(
                f"parameter {parameter} value must be [{', '.join(TransactionType.__members__.keys())}] not {value}"
            )

        if not isinstance(value, value_type):
            raise ValueError(
                f"parameter {parameter} value ({value}) is not {value_type}"
            )
        elif value_type == str:
            self.__setattr__(parameter, value.strip())
            check_string_len()

    def __post_init__(self):
        if isinstance(self.tipo, str):
            self.__setattr__("tipo", TransactionType(self.tipo).value)

        list(map(self._validate_types, self.__annotations__.items()))

        if self.valor < 0:
            raise ValueError('"valor" field cannot be negative')

        logging.debug(f"{asdict(self)}")

    def as_parameters(self):
        return self.valor, self.tipo, self.descricao

    @property
    def _realizada_em(self) -> str:
        return self.realizada_em

    @_realizada_em.setter
    def _realizada_em(self, value: str):
        self.realizada_em = value


@dataclass(repr=True)
class Balance:
    limit: int
    balance: int

    def as_transaction_response(self):
        return dict(limite=self.limit, saldo=self.balance)

    def as_statement_response(self):
        return dict(
            total=self.balance,
            data_extrato=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f"),
            limite=self.limit,
        )


@dataclass(repr=True)
class Statement:
    balance: Balance
    last_transactions: list[Transaction]

    def dicting_transactions(self, data):
        dt_object: Transaction = Transaction(
            valor=data.get("amount"),
            tipo=TransactionType(data.get("type")[0]).value,
            descricao=data.get("description"),
        )
        dt_object.realizada_em = data.get("timestamp").strftime("%Y-%m-%dT%H:%M:%S.%f")

        return dt_object.__dict__

    def __post_init__(self):
        self.saldo = self.balance.as_statement_response()
        del self.balance

        self.ultimas_transacoes = list(
            map(self.dicting_transactions, self.last_transactions)
        )
        del self.last_transactions
