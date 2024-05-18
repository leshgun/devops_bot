#!/bin/bash

sudo service ssh start
sudo chmod +r /var/log/postgresql/postgresql-16-main.log
/usr/lib/postgresql/16/bin/postgres -D /var/lib/postgresql/16/main -c "config_file=/etc/postgresql/16/main/postgresql.conf" &
service postgresql restart
sleep 2

psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}'"
psql -c "create database ${DB_DATABASE} owner ${DB_USER};"
psql -c "CREATE USER ${DB_REPL_USER} REPLICATION LOGIN ENCRYPTED PASSWORD '${DB_REPL_PASSWORD}';"
psql -c "
  CREATE TABLE IF NOT EXISTS phone (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(30) NOT NULL
  );

  CREATE TABLE IF NOT EXISTS email (
    id SERIAL PRIMARY KEY,
    email text NOT NULL
  );
" ${DB_DATABASE}
psql -c "GRANT CONNECT ON DATABASE ${DB_DATABASE} TO ${DB_USER};"
psql -c "GRANT pg_read_all_data TO ${DB_USER};" ${DB_DATABASE}
psql -c "GRANT pg_write_all_data TO ${DB_USER};" ${DB_DATABASE}
