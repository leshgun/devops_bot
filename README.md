# devops_bot

Telegram bot for storing user information in PostgreSQL, which runs in replication mode, and monitoring the database server.

## Docker

To start:

```bash
docker compose up --build
```

For configuration, you need to create a file "*.env*", which will store environment variables for containers.
An example of such a file can be found in "*.env.example*".
