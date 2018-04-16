import paramiko
from paramiko import SSHException, ssh_exception


class LoginServer(object):
    def __init__(self, target_server, port, username, password):
        self.target_server = target_server
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None

    def __enter__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.target_server,
                         port=self.port,
                         username=self.username,
                         password=self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ssh:
            self.ssh.close()

    def exec_command(self, exec_command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(exec_command)
            result = stdout.read()
            res = {'status': 'ok', 'output': result}
        except SSHException, e:
            result = str(e)
            res = {'status': 'fail', 'output': result}
        return res

if __name__ == "__main__":
    with LoginServer('10.79.148.106', 22, 'root', 'Cisco123') as p:
        test = p.exec_command("rm -rf /root/test")
        print test

