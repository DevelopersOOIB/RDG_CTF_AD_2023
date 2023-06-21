import os
from typing import Tuple

import dns.zone
import dns.update
import dns.rdataset
import dns.rdtypes
from dns.rdtypes.ANY.TXT import TXT
from paramiko import AutoAddPolicy, SSHClient
from paramiko.channel import ChannelFile, ChannelStderrFile

from custom_exceptions import SSHUnavailable


class Helper:
    TCP_CONNECTION_TIMEOUT = 15

    def __init__(self, checker, port: int = 22, container_name: str = "custom-bind"):
        self.c = checker
        self.host = checker.host
        self.port = port
        self.container_name = container_name

        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy)
        self.ssh_client.load_system_host_keys()
        self.sftp = None

    def connect(self, username: str, key_filename: str = "") -> None:
        self.ssh_client.connect(hostname=self.host,
                                username=username,
                                key_filename=key_filename,
                                disabled_algorithms=dict(keys=["ssh-ed25519", "ecdsa-sha2-nistp256",
                                                               "ecdsa-sha2-nistp384", "ecdsa-sha2-nistp521",
                                                               "ssh-dss"]))

    def connect_sftp(self) -> None:
        self.sftp = self.ssh_client.open_sftp()

    def _exec_command(self, cmd: str) -> Tuple[str, str]:
        _, stdout, stderr = self.ssh_client.exec_command(cmd)
        return stdout.read().decode(), stderr.read().decode()

    def get_container_pid(self) -> Tuple[str, str]:
        cmd = "docker inspect -f '{{{{ .State.Pid }}}}' {0}".format(self.container_name)
        stdout, stderr = self._exec_command(cmd)
        return stdout.strip(), stderr

    def get_container_mount_points(self) -> Tuple[str, str]:
        cmd = "docker inspect -f  '{{{{json .Mounts }}}}' {0}".format(self.container_name)
        stdout, stderr = self._exec_command(cmd)
        return stdout, stderr

    def rndc_reload(self, pid: str) -> Tuple[str, str]:
        cmd = f"nsenter -t {pid} -a rndc reload"
        stdout, stderr = self._exec_command(cmd)
        return stdout, stderr

    def __del__(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh_client:
            self.ssh_client.close()


class DNS:
    def __init__(self, origin: str):
        self.zone = None
        self.origin = origin

    def load_zone(self, path: str) -> None:
        self.zone = dns.zone.from_file(path, self.origin)

    def increment_serial(self):
        rdataset = self.zone.find_rdataset(self.origin, dns.rdatatype.SOA)
        rdata = rdataset[0].replace(serial=rdataset[0].serial + 1)
        new_rdataset = dns.rdataset.from_rdata(rdataset.ttl, rdata)
        self.zone.replace_rdataset(self.origin, replacement=new_rdataset)

    def append_dns_record(self, name: str, value: str, ttl: int = 86400):
        rdataset = self.zone.find_rdataset(name, dns.rdatatype.TXT, create=True)
        rdata = TXT(dns.rdataclass.IN, dns.rdatatype.TXT, value)
        rdataset.add(rdata, ttl)
