SELECT EXISTS(
        SELECT 1
        FROM clients
        WHERE id = %s
    );