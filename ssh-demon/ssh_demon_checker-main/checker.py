#!/usr/local/bin/python3
import sys
import paramiko

from requests.exceptions import ConnectionError

from checklib import status, BaseChecker, Status, cquit


class Checker(BaseChecker):
    vulns: int = 2
    timeout: int = 15
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.user = "Admin_test_user"
        self.secret = 'nYokmAIEc#4LWKrev72'
        self.port = 13564
        self.host = args[0]

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except ConnectionError as err:
            self.cquit(Status.DOWN, 'Connection error', f'Connection error, err: {err}')
        except TimeoutError as err:
            self.cquit(Status.DOWN, 'Connection error', f'Connection error, err: {err}')
        except paramiko.ssh_exception.NoValidConnectionsError as err:
            self.cquit(Status.DOWN, f'Connection error {err}', f'Connection error, err: {err}')

    def check(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.host, username=self.user, password=self.secret, port=self.port)
        stdin, stdout, stderr = client.exec_command('ls -l')
        data = stdout.read() + stderr.read()
        client.close()
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        flag_str = f"{flag_id}:{flag}"
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.host, username=self.user, password=self.secret, port=self.port)
        stdin, stdout, stderr = client.exec_command(f'echo "{flag_str}" >> flags.txt')
        data = stdout.read() + stderr.read()
        print(data)
        client.close()

        self.cquit(status.Status.OK, f'Flag put')

    def get(self, flag_id: str, flag: str, vuln: str):
        flag_str = f"{flag_id}:{flag}"
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.host, username=self.user, password=self.secret, port=self.port)
        stdin, stdout, stderr = client.exec_command('cat flags.txt')
        data = stdout.read() + stderr.read()
        client.close()
        if flag_str.split(':')[-1] not in data.decode():
            self.cquit(Status.CORRUPT, "Flags is not in flag_list")

        self.cquit(status.Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception() as e:
        cquit(Status(c.status), c.public, c.private)


