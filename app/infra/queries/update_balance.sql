update balances
set amount = amount + %(amount)s
where client_id = %(client_id)s;