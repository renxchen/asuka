# -*- coding: utf-8 -*-
# __author__ = 'yihli'

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

    
    SPILT_CHAT = u"，"

    def __init__(self, device_info, logger):
        self.device_info = device_info
        self.ip = device_info['ip']
        self.device_id = device_info['device_id']
        self.timeout = device_info.get('timeout', 10)
        #self.username = device_info.get('username')
        #self.password = device_info.get('password')
        #self.enable_password = device_info.get('enable_password')
        self.method = "Telnet"
        self.port = device_info.get('port',23)
        self.expect = device_info.get('expect')
        self.prompt = device_info.get('prompt')
        #self.default_command = device_info.get('default_commands')
        self.fail_judges = device_info.get('fail_judges',"")
        
        self.start_default_command = device_info.get('start_default_commands',"")
        self.end_default_command = device_info.get('end_default_commands',"")

        self.device_log_info = "Device ID: %s,IP: %s,HostName: %s" % (self.device_id,self.ip,device_info["hostname"])

        self.logger = logger
        self.child = None

    def login(self):
        #try:
        return self.__login()
        #except LoginException as e:
            #if e.err_code == LoginException.CONNECTION_CLOSED:
            #    if self.method == 'telnet':
            #        self.method = 'ssh'
            #    else:
            #        self.method = 'telnet'
            #    return self.__login()
            #else:
            #raise
    
    def __is_valid_command(self,output):
        
        if self.fail_judges:

            fail_strs = re.split(self.SPILT_CHAT, self.fail_judges)
            for fail_str in fail_strs:
                if re.search(fail_str,output) is not None:
                    
                    return False

            return True
        
        return True
    
    def exe_end_default_command(self):
        self.__execute_default_command(self.end_default_command)

    def __execute_default_command(self, commands):

        if not commands:
            return
        
        expect_list = [self.prompt, pexpect.TIMEOUT, pexpect.EOF]
        for command in re.split(self.SPILT_CHAT, commands):
            res = []
            self.logger.info('%s Execute default command: %s' % (self.device_log_info, command))
            self.child.sendline(command)
            i = self.child.expect(expect_list, timeout=self.timeout)
           
            if i == 1:
                #self.logger.error('%s Execute default command Timeout: %s' % (self.device_log_info,command))
                message = '%s Execute default command Timeout: %s' % (self.device_log_info,command)
                raise Exception(message)
            if i == 2:
                message = '%s Execute default command Connection_closed: %s' % (self.device_log_info,command)
                #self.logger.error('%s Execute default command Connection_closed: %s' % (self.device_log_info,command))
                raise Exception(message)
            
            if i == 0:
                res.append(self.child.before)
                res.append(str(self.child.after))
            
            output = ''.join(res)
            if not self.__is_valid_command(output):
                message = "%s Execute default command failed: %s output: %s" % (self.device_log_info,command,output)
                #self.logger.error(message)
                raise Exception(message)
            
    def __login(self):

        port = self.port or 23
        cmd_str = self.TELNET_STR % (self.ip, self.port)
  
        self.logger.info('%s Telnet Started' % self.device_log_info)
        child = pexpect.spawn(cmd_str, maxread=8192, searchwindowsize=4096)
        flag = 1
        for line in re.split(",", self.expect):
            if flag == 1:
                flag = 0
                key_word = line.encode('utf-8')
                expect_list = [key_word, pexpect.TIMEOUT, pexpect.EOF]
                i = child.expect(expect_list, timeout=self.timeout)
                if i == 1:
                    message = "%s Login Failed Timeout" % self.device_log_info
                    raise Exception(message)
                if i == 2:
                    message = "%s Connection Closed" % self.device_log_info
                    raise Exception(message)
                if i == 0:
                    continue
            elif flag == 0:
                child.sendline(line)
                flag = 1
        prompt = re.split(",", self.expect)[-1]
        self.hostname = hostname = child.before.splitlines()[-1]
        if not self.prompt:
            self.prompt = hostname + prompt

        self.child = child
        self.logger.info('%s Login success. Got device hostname: %s' % (self.device_log_info,hostname))
        self.expect_pattern = ['.*\r\n',
                               pexpect.TIMEOUT,
                               pexpect.EOF,
                               re.escape(self.prompt),
                               #'\)#',
                               #'\[confirm\]',
                               #'\]\?'
                               ]
        self.__execute_default_command(self.start_default_command)

    def execute(self, command):

        timestamp = strftime('%Y-%m-%d %H:%M:%S')
        clock = time.time()
        expect_pattern = self.expect_pattern
        child = self.child
        res = []
        timeout = self.timeout
        self.logger.info('%s Execute: %s' % (self.device_log_info, command))
        
        child.sendline(command)
        while True:
            c = child.expect(expect_pattern, timeout=timeout)
            res.append(child.before)
            res.append(str(child.after))
            if c > 0:
                break
        if c == 1:
            msg = 'Timeout'
            self.logger.error('%s Timeout execute: %s' % (self.device_log_info,command))
            raise LoginException(LoginException.LOGIN_TIMEOUT)
        output = ''.join(res)
        output = re.sub("\s*\\x08+\s*", "", output)
        output = output.replace("$rm", "")

        status = 'success'
        message = ''
        if not self.__is_valid_command(output):
            err_message = "%s Execute default command failed: %s output: %s" % (self.device_log_info,command,output)
            self.logger.error(err_message)
            message = "invalid_command"
            
        return dict(command=command, status=status, output=output, timestamp=timestamp,clock = "%f" % clock,message=message)

    def recover_prompt(self):
        expect_list = [self.prompt, pexpect.TIMEOUT, pexpect.EOF]
        self.child.sendcontrol('c')
        i = self.child.expect(expect_list, timeout=self.timeout)
        if i != 0:
            message = '%s Recover prompt failed' % (self.device_log_info)
            raise Exception(message)

    def close(self):
        try:
            # self.child.sendline('end')
            self.child.sendline('exit')
            self.child.expect([pexpect.EOF, pexpect.TIMEOUT])
            self.child.close()
            self.logger.info('%s Telnet Finished' % self.device_log_info)
        except:
            pass

if __name__ == "__main__":
    import traceback
    device_info = {
        
            #arr
            "start_default_commands": "terminal len 0，terminal pager 0",
            #arr
            "end_default_commands": "",
            "prompt":"#",
            #arr
            #"fail_judges":"% In*，Error*",
            "fail_judges":null,
            "ip": "10.71.244.135",
            "hostname": "crs1000_1",
            "expect": "ssword:,cisco,>,enable,:,cisco123,#",
            "timeout": 10,
            "device_id": "2042"
            }

    import logging as logger
    worker = CiscoCLI(device_info, logger=logger)
    output = []
    try:
        worker.login()
        commands=["show interface"]

        for index,cmd in enumerate(commands):

            try:
                cmd_out = worker.execute(cmd)
                output.append(cmd_out)
            except LoginException as e:
                if e.err_code == LoginException.LOGIN_TIMEOUT:
                    worker.recover_prompt()
                else:
                    raise
            
        worker.exe_end_default_command()

    except Exception as e:
        status = 'fail'
        message = str(e)
        logger.error(e)
    finally:
        worker.close()
    
    print output 
