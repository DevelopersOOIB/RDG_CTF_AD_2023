import paramiko

host = '192.168.157.130'
user = 'Admin_test_user'
secret = 'nYokmAIEc#4LWKrev72'
port = 13564




def check():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('ls -l')
    data = stdout.read() + stderr.read()
    print(data)
    client.close()

def putflag(flag):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command(f'echo "{flag}" > flags.txt')
    data = stdout.read() + stderr.read()
    print(data)
    client.close()

def checkflag(flag):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('cat flags.txt')
    data = stdout.read() + stderr.read()
    print(data)
    client.close()
    if flag in data:
        return True
    return False

check()
putflag("test1.flag")
print(checkflag("test1.flag"))
print(checkflag("test2.flag"))
