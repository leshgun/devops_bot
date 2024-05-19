# devops_bot

Telegram bot for storing user information in PostgreSQL, which runs in replication mode, and monitoring the database server.

## Python

For configuration, you need to create a file "*.env*", which will store environment variables for containers. An example of such a file can be found in "*.env.example*".

Also you need to install the requirements.  

```bash
pip3 install -r requirements.txt
```

It is recommended to do this in a virtual environment.

```bash
python3 -m venv ./venv
./venv/Scripts/activate
```

To start:

```bash
python3 main.py
```
