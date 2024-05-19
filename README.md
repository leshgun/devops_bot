# devops_bot

Telegram bot for storing user information in PostgreSQL, which runs in replication mode, and monitoring the database server.

## Ansible

You will need 3 machines:

1. The server for the telegram bot - Debain/Ubuntu (others platform - in future).
2. The server for the PostgreSQL - Debain 12 (others platform - in future).
3. The server for the PostgreSQL - Debain 12 (others platform - in future).

On all machines, the following must be done:

* Installed packages: *openssh-server* (or equivalent), *sudo*.
* Services running: *openssh-server*
* A user must be created for Ansible with password (as in the file *env_example.yaml*).
* The Ansible-user must be a superuser (there must be an entry like `<username> ALL=(ALL:ALL) NOPASSWD: ALL` in the file */etc/sudoers*)

To start:

```bash
ansible-playbook playbook_tg_bot.yml -e @env.yaml
```

For configuration, you need to create a file "env.yaml", which will store environment variables for machines.
An example of such a file can be found in "*env.yaml.example*".
