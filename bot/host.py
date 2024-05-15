""" Host """

import paramiko

class Host:
    """ Creating the Host class """

    def __init__(self, host: str, port = 22, login = 'root', password = ''):
        self.host = host
        self.port = port
        self.login = login
        self._password = password
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        """Some docstrings..."""
        self._client.connect(
            hostname=self.host,
            port=self.port,
            username=self.login,
            password=self._password
        )

    def exec(self, command: str):
        """Some docstrings..."""
        _, stdout, stderr = self._client.exec_command(command)
        data = stdout.read() + stderr.read()
        data = data.decode("utf-8")
        return str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]

    def close(self):
        """Some docstrings..."""
        self._client.close()
