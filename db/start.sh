#!/bin/bash

sudo service ssh start
sudo chmod +r /var/log/postgresql/postgresql-16-main.log
/usr/lib/postgresql/16/bin/postgres -D /var/lib/postgresql/16/main -c "config_file=/etc/postgresql/16/main/postgresql.conf" &
service postgresql restart
sleep 2

psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}'"
psql -c "create database ${DB_DATABASE} owner postgres;"
psql -c "CREATE USER ${DB_REPL_USER} REPLICATION LOGIN ENCRYPTED PASSWORD '${DB_REPL_PASSWORD}';"
psql $DB_DATABASE < /app/sqlfile.sql
