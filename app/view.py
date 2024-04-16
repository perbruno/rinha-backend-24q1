from services.view_adapter import Transaction, Balance, Statement
from controller import get_client_statement, create_client_transaction
from services.logging import logging

from flask import Flask, request, jsonify

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/healthcheck")
def healthcheck():
    return "Hello,World!"


@app.route("/clientes/<int:id>/transacoes", methods=["POST"])
def post_transactions(id):
    try:
        amount, transaction_type, description = Transaction(
            **request.get_json()
        ).as_parameters()
    except ValueError as verr:
        return verr.__str__(), 422

    try:
        response = create_client_transaction(
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            client_id=id,
        )
        return jsonify(Balance(**response).as_transaction_response())
    except IndexError as ierr:
        return ierr.__str__(), 404
    except ValueError as verr:
        return verr.__str__(), 422
    except BaseException as err:
        return err.__str__(), 500


@app.route("/clientes/<int:id>/extrato", methods=["GET"])
def get_statement(id):
    try:
        statement = get_client_statement(client_id=id)
        dt_statement = Statement(
            balance=Balance(**statement.get("balance")),
            last_transactions=statement.get("last_transactions"),
        )
        return jsonify(dt_statement.__dict__)
    except IndexError as ierr:
        return ierr.__str__(), 404
    except ValueError as verr:
        return verr.__str__(), 422
    except BaseException as err:
        return err.__str__(), 500


if __name__ == "__main__":
    app.run(debug=True)
