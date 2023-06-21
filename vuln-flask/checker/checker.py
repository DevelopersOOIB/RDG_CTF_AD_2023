#!/usr/local/bin/python3.9

import sys
from typing import Tuple, Optional
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import ConnectionError
from checklib import status, BaseChecker, generators, Status, cquit

from helper import Helper


class Checker(BaseChecker):
    vulns: int = 2
    timeout: int = 15
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.helper = Helper(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except ConnectionError as err:
            self.cquit(Status.DOWN, 'Connection error', f'Got requests connection error, err: {err}')

    def check(self):
        username = generators.rnd_username(5)
        password = generators.rnd_password(10)

        response: Response = self.helper.register(username, password)
        if 'Congratulations, you are now a registered user!' not in response.text:
            self.cquit(Status.MUMBLE, "Register failed", f"Register failed: {response.text}")

        if 'Please use a different username.' in response.text:
            self.cquit(Status.MUMBLE, "Register failed", "Such user already exist")

        response: Response = self.helper.login(username, password)
        if 'Invalid username or password' in response.text:
            self.cquit(Status.MUMBLE, "Login failed", "Invalid username or password for new user")

        token = response.cookies.get('access_token')
        if token is None:
            self.cquit(Status.MUMBLE, "Failed to get access token", "Cookie 'access_token' is empty")

        response: Response = self.helper.profile()
        if 'Profile' not in response.text:
            self.cquit(Status.MUMBLE, "Profile failed", "Failed to check profile")

        soup = BeautifulSoup(response.text, features="html.parser")
        input_tag = soup.find(id='userid')
        user_id = input_tag['value']
        payload = f"<root><user><username>{username}1</username>" \
                  f"<email></email>" \
                  f"<bio>Checker</bio></user></root>"
        response: Response = self.helper.profile_api(user_id, token, payload)
        try:
            root = ET.fromstring(response.text)
            bio = root.find('user/bio').text
            if bio != 'Checker':
                self.cquit(Status.MUMBLE, "Profile API failed", "Failed to check profile API entrypoint")
        except Exception:
            self.cquit(Status.MUMBLE, "Profile API failed", "Failed to check profile API entrypoint")

        response: Response = self.helper.check_es(token)
        data = response.json()
        hostname = data.get('hostname')
        if hostname != 'http://custom-es:9200':
            self.cquit(Status.MUMBLE, f"Unknown ES hostname", f"ES hostname was changed: {hostname}")

        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        username = generators.rnd_username(5)
        password = generators.rnd_password(10)

        self.helper.register(username, password)
        response: Response = self.helper.login(username, password)

        token = response.cookies.get('access_token')
        if token is None:
            self.cquit(Status.MUMBLE, "Failed to get access token", "Cookie 'access_token' is empty")

        response: Response = self.helper.create_flag(token, flag)
        if response.status_code not in [200, 201]:
            self.cquit(Status.MUMBLE, "Failed create a new flag", response.text)

        data = response.json()
        fid = data.get('id')
        if fid is None:
            self.cquit(Status.MUMBLE, "Failed to get flag id from response", response.text)

        self.cquit(status.Status.OK, username, f'{username}*{fid}*{token}')

    def get(self, flag_id: str, flag: str, vuln: str):
        _, flag_id, token = flag_id.split('*')

        response: Response = self.helper.get_flag(flag_id, token)
        if response.status_code != 200:
            self.cquit(Status.MUMBLE, "Failed to get existing flag", response.text)

        data = response.json()
        if data.get('flag') is None:
            self.cquit(Status.MUMBLE, "Failed to get flag id from response", response.text)

        if data.get('flag') != flag:
            self.cquit(Status.CORRUPT, "Flags not equal", response.text)

        self.cquit(status.Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception() as e:
        cquit(Status(c.status), c.public, c.private)
