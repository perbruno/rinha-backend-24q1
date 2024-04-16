select * from transactions
where client_id = %(id)s
ORDER BY created_at DESC
LIMIT %(limit)s;