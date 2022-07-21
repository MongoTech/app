from typing import Union

from paramiko import client


class Connection:
    client = None

    def __init__(self, hostname: str, username: str, key_filename: str) -> None:
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(
            hostname=hostname, username=username, key_filename=key_filename
        )

    def sending_commands(self, command: str) -> Union[str, bool]:
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)  # nosec

            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)

                    while stdout.channel.recv_ready():
                        alldata += stdout.channel.recv(1024)

                    return str(alldata, "utf8")
        return False
