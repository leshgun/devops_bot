# devops_bot

Telegram bot for storing user information in PostgreSQL, which runs in replication mode, and monitoring the database server.

## Ansible

To start:

```bash
ansible-playbook playbook_tg_bot.yml -e @env.yaml
```

For configuration, you need to create a file "env.yaml", which will store environment variables for containers.
An example of such a file can be found in "*env.yaml.example*".
