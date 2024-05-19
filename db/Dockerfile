FROM ubuntu

# Environment with default value
ARG DB_USER=master
ARG DB_PASSWORD=qwerty123
ARG DB_REPL_USER=repl_user
ARG DB_REPL_PASSWORD=qwerty123
ARG DB_PORT=5432
ARG DB_DATABASE=mybot

ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_REPL_USER=$DB_REPL_USER
ENV DB_REPL_PASSWORD=$DB_REPL_PASSWORD
ENV DB_PORT=$DB_PORT
ENV DB_DATABASE=$DB_DATABASE

WORKDIR /app

COPY start.sh .
RUN chmod +x start.sh


RUN apt-get update && apt-get install openssh-server postgresql postgresql-contrib sudo -y --no-install-recommends

RUN useradd -rm -d /home/$DB_USER -s /bin/bash -g root -G sudo -u 1001 $DB_USER
RUN echo "$DB_USER:$DB_PASSWORD" | chpasswd

RUN echo "postgres   ALL = (ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "$DB_DATABASE" && sleep 5

RUN echo 'archive_mode = on' >> /etc/postgresql/16/main/postgresql.conf
RUN echo "archive_command = 'cp %p /oracle/pg_data/archive/%f'" >> /etc/postgresql/16/main/postgresql.conf
RUN echo 'max_wal_senders = 10' >> /etc/postgresql/16/main/postgresql.conf
RUN echo 'wal_level = replica' >> /etc/postgresql/16/main/postgresql.conf
RUN echo 'wal_log_hints = on' >> /etc/postgresql/16/main/postgresql.conf
RUN echo 'log_replication_commands = on' >> /etc/postgresql/16/main/postgresql.conf
RUN echo "host replication $DB_REPL_USER 0.0.0.0/0 scram-sha-256" >> /etc/postgresql/16/main/pg_hba.conf
RUN echo "listen_addresses = '*'" >> /etc/postgresql/16/main/postgresql.conf

RUN mkdir -p /oracle/pg_data/archive/
RUN chown postgres:postgres /oracle/pg_data/archive/

EXPOSE 22
EXPOSE 5432

user postgres
CMD ["/bin/bash", "-c", "/app/start.sh && tail -f /dev/null"]

