INSERT INTO transactions(client_id, category, amount, description)
values (
        %(client_id)s,
        %(category)s,
        %(amount)s,
        %(description)s
    );