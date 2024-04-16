select amount, client_limit
from balances
where client_id = %s;