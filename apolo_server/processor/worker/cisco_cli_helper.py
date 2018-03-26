# __author__ = 'zhutong'

# ##########################################################
# Script for collecting information from Cisco devices
# pexpect is required & openSSH is tested.
# ##########################################################

import re
from time import strftime

import pexpect
import re
import time


def replace_spec_character(after_str, line, others_str=[], is_utf_8=True):
    spec_list = ['\x08', '\x1B[K', '\x1B', '[7m', '[m', '\x1B[7m\x1B[m']
    spec_list.extend(others_str)
    for each in spec_list:
        line = str(line).replace(each, after_str)
    if is_utf_8:
        return line.decode('utf-8', 'replace')
    return line


class LoginException(Exception):
    LOGIN_TIMEOUT = -1
    CONNECTION_CLOSED = -2
    LOGIN_FAILED = -3
    ENABLE_FAILED = -4

    __message = {LOGIN_TIMEOUT: 'Timeout',
                 CONNECTION_CLOSED: 'Connection Closed',
                 LOGIN_FAILED: 'Wrong username or password',
                 ENABLE_FAILED: 'Wrong enable password',
                 }

    def __init__(self, err_code):
        self.err_code = err_code
        self.err_msg = self.__message[err_code]

    def __str__(self):
        return '<LoginException.%s>' % self.err_msg


class CiscoCLI(object):
    TELNET_STR = 'telnet %s %d'
    SSH_STR = 'ssh -p %d -o "UserKnownHostsFile /dev/null" -l %s %s'

    def __init__(self, device_info, logger):
        self.device_info = device_info
        self.ip = device_info['ip']
        self.timeout = device_info.get('timeout', 10)
        self.username = device_info.get('username')
        self.password = device_info.get('password')
        self.enable_password = device_info.get('enable_password')
        self.method = device_info.get('method', 'ssh').lower()
        self.port = device_info.get('port')
        self.expect = device_info.get('expect')
        self.default_command = device_info.get('default_commands')
        self.logger = logger
        self.child = None

    def login(self):
        try:
            return self.__login()
        except LoginException as e:
            if e.err_code == LoginException.CONNECTION_CLOSED:
                if self.method == 'telnet':
                    self.method = 'ssh'
                else:
                    self.method = 'telnet'
                return self.__login()
            else:
                raise

    def __default_command(self, commands):
        for command in re.split(";", "terminal len 0;terminal pager 0"):
            self.logger.info('%s execute default: %s' % (self.ip, command))
            self.child.sendline(command)
            self.child.expect(self.prompt, timeout=self.timeout)

    def __login(self):
        ip = self.ip
        method = self.method
        username = self.username
        timeout = self.timeout
        default_command = self.default_command
        expect = self.expect
        port = self.port
        child = self.child
        if method == 'telnet':
            port = port or 23
            cmd_str = self.TELNET_STR % (ip, port)
        else:
            port = port or 22
            cmd_str = self.SSH_STR % (port, username, ip)
        self.logger.info('%s %s' % (method, ip))
        child = pexpect.spawn(cmd_str, maxread=8192, searchwindowsize=4096)
        flag = 1
        for line in re.split(",", expect):
            if flag == 1:
                flag = 0
                key_word = line.encode('utf-8')
                expect_list = [key_word, pexpect.TIMEOUT, pexpect.EOF]
                i = child.expect(expect_list, timeout=timeout)
                if i == 1:
                    raise LoginException(LoginException.LOGIN_TIMEOUT)
                if i == 2:
                    raise LoginException(LoginException.CONNECTION_CLOSED)
                if i == 0:
                    continue
            elif flag == 0:
                child.sendline(line)
                flag = 1
        prompt = re.split(",", expect)[-1]
        self.hostname = hostname = child.before.splitlines()[-1]
        self.prompt = hostname + prompt
        self.child = child
        self.logger.info('%s %s success. Got hostname: %s' % (method,
                                                              ip,
                                                              hostname))
        self.expect_pattern = ['.*\r\n',
                               pexpect.TIMEOUT,
                               pexpect.EOF,
                               re.escape(self.prompt),
                               '\)#',
                               '\[confirm\]',
                               '\]\?']
        self.__default_command(self.default_command)

    def execute(self, command):

        timestamp = strftime('%Y-%m-%d %H:%M:%S')
        clock = time.time()
        expect_pattern = self.expect_pattern
        child = self.child
        res = []
        timeout = self.timeout
        self.logger.info('%s execute: %s' % (self.ip, command))
        child.sendline(command)
        while True:
            c = child.expect(expect_pattern, timeout=timeout)
            res.append(child.before)
            res.append(str(child.after))
            if c > 0:
                break
        if c == 1:
            msg = 'Timeout'
            self.logger.error('Timeout execute: %s @ %s' % (command, self.ip))
            raise Exception(msg)
        output = ''.join(res)
        output = re.sub("\s*\\x08+\s*", "", output)
        output = output.replace("$rm", "")
        if " '^' " in output:
            status = 'Error'
        else:
            status = 'Ok'
        
        return dict(command=command, status=status, output=output, timestamp=timestamp,clock=clock)

    def close(self):
        try:
            # self.child.sendline('end')
            self.child.sendline('exit')
            self.child.expect([pexpect.EOF, pexpect.TIMEOUT])
            self.child.close()
            self.logger.info('Disconnected from %s' % self.ip)
        except:
            pass
