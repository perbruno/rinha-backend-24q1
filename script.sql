create table if not exists clients (
  id SERIAL primary key,
  name VARCHAR(30) not null UNIQUE,
  created_at TIMESTAMP not null default timezone('utc', now())
);

create table if not exists balances (
  id SERIAL primary key,
  client_id INT4 not null references clients(id) UNIQUE,
  amount INT4 not null default 0,
  client_limit INT4 not null,
  created_at TIMESTAMP not null default timezone('utc', now()),
  updated_at TIMESTAMP not null default timezone('utc', now())
);

create or replace
function update_balance_data()
returns trigger
language PLPGSQL
as
$$
begin
NEW.updated_at = timezone('utc', now());

return new;
end
$$;

create or replace
trigger balance_updated
before
update
	on
	balances
for each row
execute procedure update_balance_data();

create type transactionType as enum ('credit','debit');

create table if not exists transactions (
  id SERIAL primary key,
  client_id INT4 not null references clients(id),
  category transactionType,
  amount INT4 not null,
  description VARCHAR(10) not null,
  created_at TIMESTAMP not null default timezone('utc', now())
);


do $$
begin
  insert into
	clients (name)
values
    ('o barato sai caro'),
    ('zan corp ltda'),
    ('les cruders'),
    ('padaria joia de cocaia'),
    ('kid mais');
end$$;

do $$
begin
  insert into
	balances(client_id,
	amount,
	client_limit)
values
  (1, 0, 1000 * 100),
  (2, 0, 800 * 100),
  (3, 0, 10000 * 100),
  (4, 0, 100000 * 100),
  (5, 0, 5000 * 100);
end;
$$