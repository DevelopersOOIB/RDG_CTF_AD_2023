#!/usr/local/bin/python3
import sys
import json
import logging
import os.path
from typing import Optional

import dns.resolver
import paramiko
from dns.exception import DNSException
from dns.resolver import LifetimeTimeout, NoNameservers
from socket import gaierror
from checklib import status, BaseChecker, generators, Status, cquit
from paramiko.ssh_exception import NoValidConnectionsError, SSHException
from paramiko.pkey import PKey

from helper import Helper, DNS
from custom_exceptions import SSHUnavailable


# Dynamic variables
USERNAME = "root"
SERVICE_NAME = "dns"
PRIVATE_KEY = "dns_key"

# Static variables
CONTAINER_NAME = "custom-bind"
ZONE_PATH = f"/checkers/{SERVICE_NAME}/zones"
KEY_FILENAME = f"/checkers/{SERVICE_NAME}/dns_key"

# Logging
f = open(os.devnull, 'w')
logging.basicConfig(
    stream=f,
    level=logging.DEBUG
)


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 15
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        self.container_name = CONTAINER_NAME
        super(Checker, self).__init__(*args, **kwargs)
        self.helper = Helper(self)
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = [self.helper.host]

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except (NoValidConnectionsError, LifetimeTimeout, EOFError, gaierror) as err:
            from traceback import format_exc
            self.cquit(Status.DOWN, 'Connection error',
                       f'Got requests connection error, err: {err}, trace: {format_exc()}')

    def check(self):
        try:
            dns.resolver.resolve("rdg-ctf2023.local.", "NS")
        except NoNameservers as err:
            # All nameservers failed to answer the query ... IN NS: Server ... UDP port 53 answered REFUSED
            self.cquit(Status.DOWN, f"{err}", f"{err}")

        try:
            self.helper.connect(username=USERNAME, key_filename=KEY_FILENAME)
        except (NoValidConnectionsError, ValueError, SSHException) as err:
            self.cquit(Status.MUMBLE, "SSH service is unavailable",  f"SSH service is unavailable: {err}")

        stdout, stderr = self.helper.get_container_pid()
        if not stdout.isnumeric():
            self.cquit(Status.DOWN, "Container is unavailable", f"Container is unavailable. Errors: {stderr}")

        stdout, stderr = self.helper.get_container_mount_points()
        mounts = json.loads(stdout)
        remote_zone_path = self._get_remote_zone_path(mounts)
        if remote_zone_path is None:
            self.cquit(Status.MUMBLE,
                       "DNS zone file is unavailable in mount points",
                       "Could not found zone file '/etc/bind/zones/rdg-ctf2023.zone' in mount points")
        try:
            self.helper.connect_sftp()
        except SSHUnavailable:
            self.cquit(Status.MUMBLE, "Cannot open sftp connection", "Cannot open sftp connection")

        rnd = generators.rnd_string(6)
        local_zone_path = f'{rnd}_rdg-ctf2023.zone'
        try:
            self.helper.sftp.get(remote_zone_path, os.path.join(ZONE_PATH, local_zone_path))
            os.remove(os.path.join(ZONE_PATH, local_zone_path))
        except FileNotFoundError:
            self.cquit(Status.MUMBLE, f"Cannot find zone file", f"Cannot find zone file '{remote_zone_path}'")
        except PermissionError:
            self.cquit(Status.MUMBLE, f"Permission denied when downloading a file '{remote_zone_path}'",
                       f"Permission denied when downloading a file '{remote_zone_path}'")

        self.cquit(Status.OK)

    def get(self, flag_id: str, flag: str, vuln: str):
        answer = None
        try:
            answer = dns.resolver.resolve(flag_id, "TXT")
        except LifetimeTimeout as err:
            self.cquit(Status.CORRUPT, "The resolution lifetime expired", f"The resolution lifetime expired: {err}")
        except dns.resolver.NXDOMAIN as err:
            self.cquit(Status.CORRUPT, "Failed to get flag from response", f"Failed to get flag from response: {err}")
        except Exception as err:
            self.cquit(Status.CORRUPT, "Unexpected exception. Сontact the organizers",  f"Unexpected exception: {err}")

        if answer is None:
            self.cquit(Status.CORRUPT, "Failed to get flag", f"Failed to get flag")

        answer = answer[0].to_text().strip("\"")
        if answer != flag:
            self.cquit(Status.CORRUPT, "Flags are not equal", f"Flags are not equal: {answer} != {flag}")

        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        try:
            self.helper.connect(username=USERNAME, key_filename=KEY_FILENAME)
        except (NoValidConnectionsError, SSHException, ValueError) as err:
            self.cquit(Status.MUMBLE, "SSH service is unavailable",  f"SSH service is unavailable: {err}")

        self.helper.connect(username=USERNAME, key_filename=KEY_FILENAME)

        pid, stderr = self.helper.get_container_pid()
        if not pid.isnumeric():
            self.cquit(Status.DOWN, "Container is unavailable", f"Container is unavailable. Errors: {stderr}")

        stdout, stderr = self.helper.get_container_mount_points()
        mounts = json.loads(stdout)
        remote_zone_path = self._get_remote_zone_path(mounts)
        if remote_zone_path is None:
            self.cquit(Status.MUMBLE,
                       "DNS zone file is unavailable in mount points",
                       "Could not found zone file '/etc/bind/zones/rdg-ctf2023.zone' in mount points")

        try:
            self.helper.connect_sftp()
        except SSHUnavailable:
            self.cquit(Status.MUMBLE, "Cannot open sftp connection", "Cannot open sftp connection")

        rnd = generators.rnd_string(6)
        local_zone_path = f'{rnd}_rdg-ctf2023.zone'
        try:
            self.helper.sftp.get(remote_zone_path, os.path.join(ZONE_PATH, local_zone_path))
        except FileNotFoundError:
            self.cquit(Status.MUMBLE, f"Cannot find zone file", f"Cannot find zone file '{remote_zone_path}'")
        except PermissionError:
            self.cquit(Status.MUMBLE, f"Permission denied when downloading a file '{remote_zone_path}'",
                       f"Permission denied when downloading a file '{remote_zone_path}'")

        origin = "rdg-ctf2023.local."
        d = DNS(origin)
        try:
            d.load_zone(os.path.join(ZONE_PATH, local_zone_path))
        except DNSException as err:
            self.cquit(Status.MUMBLE, "Cannot to load zone", f"Cannot to load zone '{err}'")

        # Add new txt record
        name = generators.rnd_string(7)
        d.append_dns_record(name, flag)
        d.increment_serial()

        # Save updated zone
        d.zone.to_file(os.path.join(ZONE_PATH, local_zone_path), want_origin=True)

        # Update zone on remote server
        self.helper.sftp.put(os.path.join(ZONE_PATH, local_zone_path), remote_zone_path)

        # Remove send file
        os.remove(os.path.join(ZONE_PATH, local_zone_path))

        # Reload named zone
        stdout, stderr = self.helper.rndc_reload(pid)
        if stderr:
            self.cquit(Status.MUMBLE, "Cannot reload dns server", f"Cannot reload dns server: {stderr}")

        self.cquit(status.Status.OK, f"{name}.{origin}")

    @staticmethod
    def _get_remote_zone_path(mounts: dict) -> Optional[str]:
        remote_zone_path = None
        for mount in mounts:
            if mount.get('Type') == "bind" and mount.get('Destination') == "/etc/bind/zones/rdg-ctf2023.zone":
                remote_zone_path = mount.get('Source')
        return remote_zone_path


if __name__ == '__main__':
    c = Checker(sys.argv[2])
    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception() as e:
        cquit(Status(c.status), c.public, c.private)
    f.close()
