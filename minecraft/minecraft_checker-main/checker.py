#!/usr/local/bin/python3
import sys
from requests.exceptions import ConnectionError

from checklib import status, BaseChecker, Status, cquit

import minecraft_helper


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 15
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.port = 25565
        self.host = args[0]

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except ConnectionError as err:
            self.cquit(Status.DOWN, 'Connection error', f'Connection error, err: {err}')
        except TimeoutError as err:
            self.cquit(Status.DOWN, 'Connection error', f'Connection error, err: {err}')
        except ConnectionRefusedError as err:
            self.cquit(Status.DOWN, 'Connection error', f'Connection error, err: {err}')

    def check(self):
        username = "Admin_user_files"
        password = ""
        Checker = minecraft_helper.Minecraft(username, password, self.host, self.port)
        Checker.connect()
        Checker.disconnect()
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        username = flag
        password = ""
        Checker = minecraft_helper.Minecraft(username, password, self.host, self.port)
        Checker.connect()
        Checker.disconnect()
        self.cquit(status.Status.OK, f'Flag put')

    def get(self, flag_id: str, flag: str, vuln: str):
        username = flag
        password = ""
        Checker = minecraft_helper.Minecraft(username, password, self.host, self.port)
        Checker.connect()
        Checker.disconnect()
        self.cquit(status.Status.OK, f'Flag put')


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception() as e:
        cquit(Status(c.status), c.public, c.private)
