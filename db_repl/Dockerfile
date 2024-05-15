FROM ubuntu

ARG DB_HOST=db
ARG DB_PORT=5432
ARG DB_REPL_USER=repl_user
ARG DB_REPL_PASSWORD=qwerty123

ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV DB_REPL_USER=$DB_REPL_USER
ENV DB_REPL_PASSWORD=$DB_REPL_PASSWORD

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install postgresql postgresql-contrib sudo -y --no-install-recommends
RUN chmod 777 /app/start.sh

RUN echo "listen_addresses = '*'" >> /etc/postgresql/16/main/postgresql.conf
RUN service postgresql stop
RUN rm -rf /var/lib/postgresql/16/main/*

user postgres
RUN echo "$DB_HOST:$DB_PORT:$DB_REPL_USER:$DB_REPL_PASSWORD" > ~/.pgpass
CMD ["/bin/bash", "-c", "/app/start.sh  && tail -f /dev/null"]

#
