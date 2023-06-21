#!/usr/local/bin/python3
from ast import main
import sys
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError

from src.helping import CheckFabric
from checklib import status, BaseChecker, generators, Status, cquit

class Checker(BaseChecker):
    vulns: int = 2
    timeout: int = 15
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.check_method_fabric = CheckFabric(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except ConnectionError as err:
            self.cquit(Status.DOWN, 'Connection error', f'Got requests connection error, err: {err}')

    def check(self):
        username = generators.rnd_username(5)
        password = generators.rnd_password(10)
        new_password = generators.rnd_password(10)
        auth = HTTPBasicAuth(username, password)

        self.check_method_fabric.signup(username, password)
        self.check_method_fabric.signin(username, password)
        self.check_method_fabric.actuator(auth)
        self.check_method_fabric.link(auth)
        self.check_method_fabric.create_note(auth)
        self.check_method_fabric.check_note_filter(auth)
        self.check_method_fabric.check_note_sort(auth)
        self.check_method_fabric.change_password(auth, new_password)
        
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        username = generators.rnd_username(5)
        password = generators.rnd_password(10)
        auth = HTTPBasicAuth(username, password)

        self.check_method_fabric.signup(username, password)
        self.check_method_fabric.signin(username, password)
        internal_flag_id = self.check_method_fabric.create_flag(auth, flag_id, flag)
        
        self.cquit(status.Status.OK, username, f'{username}*{password}*{flag_id}*{internal_flag_id}')


    def get(self, flag_id: str, flag: str, vuln: str):
        username, password, flag_id, internal_flag_id = flag_id.split('*')
        auth = HTTPBasicAuth(username, password)
        self.check_method_fabric.get_flag(auth, flag_id, internal_flag_id, flag)
        
        self.cquit(status.Status.OK)

if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception() as e:
        cquit(Status(c.status), c.public, c.private)
