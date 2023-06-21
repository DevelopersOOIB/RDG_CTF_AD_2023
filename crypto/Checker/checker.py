#!/usr/local/bin/python3
import sys
import socket
import os
import signal
import subprocess
from time import sleep
from typing import Tuple, Optional
from requests import Response
from requests.exceptions import ConnectionError

from checklib import status, BaseChecker, generators, Status, cquit


class Checker(BaseChecker):
    vulns: int = 2
    timeout: int = 40
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.port = 9990
        self.host = args[0]
        self.key, self.seed = self.creds()

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except ConnectionError as err:
            self.cquit(Status.DOWN, 'Connection error', f'Got requests connection error, err: {err}')
        except ConnectionRefusedError as err:
            self.cquit(Status.DOWN, 'Connection refused', f'Connection Refused Error: {err}')
        except BrokenPipeError as err:
            self.cquit(Status.DOWN, 'BrokenPipeError', f'BrokenPipeError: {err}')
        except ValueError as err:
            self.cquit(Status.DOWN, 'ValueError', f'ValueError: {err}')
        
    def open_file(self, DC=None):
        with open(f'/checkers/crypto_task_RDG23/Checker/{DC}/key.txt', 'r') as file:
            key = [int(i) for i in file.read().split(', ')]
        with open(f'/checkers/crypto_task_RDG23/Checker/{DC}/seed.txt', 'r') as file:
            seed = [int(i) for i in file.read().split(', ')]
        return key, seed

    def creds(self):
        print(self.host)
        host_ip=self.host
        print(host_ip)
        if (host_ip == "10.20.1.5"):
            key, seed = self.open_file('DC_1')
        if (host_ip == "10.20.2.5"):
            key, seed = self.open_file('DC_2')
        if (host_ip == "10.20.3.5"):
            key, seed = self.open_file('DC_3')
        if (host_ip == "10.20.4.5"):
            key, seed = self.open_file('DC_4')
        if (host_ip == "10.20.5.5"):
            key, seed = self.open_file('DC_5')
        if (host_ip == "10.20.6.5"):
            key, seed = self.open_file('DC_6')
        if (host_ip == "10.20.7.5"):
            key, seed = self.open_file('DC_7')
        if (host_ip == "10.20.8.5"):
            key, seed = self.open_file('DC_8') 
        if (host_ip == "10.20.9.5"):
            key, seed = self.open_file('DC_9')
        if (host_ip == "10.20.10.5"):
            key, seed = self.open_file('DC_10')
        return key, seed
    
    def check(self):
        HOST = self.host
        PORT = self.port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.recv(1024)
            s.send(b'1\n')
            s.recv(1024)
            s.send(b'222143822930790612718870312352643049934213650124885769687499809174244824650622443634964024817005429695992896157843803574821156064906280354764292792068618186937440439957481845591289667799935817705554164498620045892983963377688021408943782884507570379242115999381473375472819884518896184509387942780266816257079\n')
            s.recv(1024)
            s.send(b'33636184115506839989007879046339461175591491723650104565906649522884907872643930813332879520829363975042562510588746381651685542024191576175085544118094490358463666100524147294576134860478782189808069960706280154736051567068661081384866812143832055243114380792342785408790302895505802889844018527901813875171\n')
            s.recv(1024)
            s.send(b'130500766432097758106086835916511998278828815871446000465855737560554447314785196096197546393492387925672713782713802293418969602588154780941436855068321948585895333244825172667190134434154507986316890981275611676272406117613469303479976155060089727504051617080146930222616335592415622403426812294985602773194\n')
            s.recv(1024)
            s.send(b'hello\n')
            s.recv(1024)
            s.send(b'3\n')
            s.recv(1024)
            s.send(b'4\n')
            cmd = f"ncat {HOST} 7777 > /tmp/log.txt"
            pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            sleep(2)
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
            s.recv(1024)
            s.send(b'0\n')

            if os.path.exists("/tmp/log.txt"):
                os.remove('/tmp/log.txt')  
                self.cquit(Status.OK)
            else:
                self.cquit(Status.MUMBLE, "The problem with sending the log file on the team side")

        

    def put(self, flag_id: str, flag: str, vuln: str):
        HOST = self.host
        PORT = self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.recv(1024)
            s.send(b'1\n')
            s.recv(1024)
            s.send(b'222143822930790612718870312352643049934213650124885769687499809174244824650622443634964024817005429695992896157843803574821156064906280354764292792068618186937440439957481845591289667799935817705554164498620045892983963377688021408943782884507570379242115999381473375472819884518896184509387942780266816257079\n') # заменить на ключи предоставляемые серегой
            s.recv(1024)
            s.send(b'33636184115506839989007879046339461175591491723650104565906649522884907872643930813332879520829363975042562510588746381651685542024191576175085544118094490358463666100524147294576134860478782189808069960706280154736051567068661081384866812143832055243114380792342785408790302895505802889844018527901813875171\n') # заменить на ключи предоставляемые серегой
            s.recv(1024)
            s.send(b'130500766432097758106086835916511998278828815871446000465855737560554447314785196096197546393492387925672713782713802293418969602588154780941436855068321948585895333244825172667190134434154507986316890981275611676272406117613469303479976155060089727504051617080146930222616335592415622403426812294985602773194\n') # заменить на ключи предоставляемые серегой
            s.recv(1024)
            s.send(bytes('{}\n'.format(flag), encoding='utf8'))
            s.recv(1024)
            s.send(b'0\n')

        self.cquit(Status.OK, 'Flag put')

    def rand_bit(self):
        new_bit = 0
        for i in range(1, len(self.key)):
            if self.key[i] == 1:
                new_bit ^= self.seed[-i]
        self.seed = self.seed[1: ] + [new_bit]
        return new_bit

    def rand(self, L):
        res = 0
        for i in range(L):
            res = (res << 1) ^ self.rand_bit()
        return res

    def get(self, flag_id: str, flag: str, vuln: str):

        HOST = self.host
        PORT = self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.recv(1024)    
            s.send(b'4\n')
            cmd = f"ncat {HOST} 7777 > /tmp/log.txt"
            pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            sleep(20)
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
            s.recv(1024)
            s.send(b'0\n')
        
        with open('/tmp/log.txt', 'r') as f:
            for line in f:
                if line != '' or line != ' ':            
                    continue
                else:
                    self.cquit(Status.CORRUPT, "Missing flags", "An empty log file was downloaded")


        presence = 0
        with open('/tmp/log.txt', 'r', encoding="utf-8") as file:
            messages = file.readlines()
        for i in range(0, len(messages), 2):
            p, g, y = [int(j) for j in messages[i].split('=')[1].split(', ')]
            a, b = [int(j) for j in messages[i+1].split(':')[1].split(', ')]
            k = self.rand(512)
            m = (b*pow(y, -k, p)) % p 
            print(m.to_bytes(len(bin(m)[2:])//8 + 1, byteorder = 'big'))                 
            if m.to_bytes(len(bin(m)[2:])//8 + 1, byteorder = 'big') == bytes('{}'.format(flag), encoding='utf-8'):
                presence += 1
        os.remove('/tmp/log.txt')
        if presence > 0:
            self.cquit(Status.OK, "Status OK")
        else:
            self.cquit(Status.CORRUPT, "Missing flags", "There is a possibility that the file did not have time to be fully checked due to its large volume")


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception() as e:
        cquit(Status(c.status), c.public, c.private)
