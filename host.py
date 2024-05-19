""" Host """

import paramiko

class Host:
    """ Creating the Host class """

    def __init__(self, host: str, port = 22, login = 'root', password = '', 
                 **kwargs):
        self.host = host
        self.port = port
        self.login = login
        self.logger = kwargs.get('logger', lambda: None)
        self._password = password
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.logger.info(f'Host {self.host} has been initialized.')

    def connect(self):
        """Some docstrings..."""
        self._client.connect(
            hostname=self.host,
            port=self.port,
            username=self.login,
            password=self._password
        )
        self.logger.info(f'Client has been connected to host {self.host}.')

    def exec(self, command: str):
        """Some docstrings..."""
        self.logger.info(f'Sending command "{self.host}" to host "{self.host}".')
        _, stdout, stderr = self._client.exec_command(command)
        data = stdout.read() + stderr.read()
        data = data.decode("utf-8")
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        self.logger.info(f'--- Response: "{data}"')
        return data

    def close(self):
        """Some docstrings..."""
        self._client.close()
        self.logger.info('The connection is closed.')
