#!/bin/bash

sleep 10

echo $DB_REPL_PASSWORD | pg_basebackup -R -h $DB_HOST -p $DB_PORT -U $DB_REPL_USER -D /var/lib/postgresql/16/main -P

service postgresql start
