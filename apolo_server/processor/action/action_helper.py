import subprocess
import time
from apolo_server.processor.constants import ActionConstants


class CommandTimeoutError(Exception):
    def __init__(self, msg):
        self.message = msg
        pass

    def __str__(self):
        return self.message


class ActionError(Exception):
    def __init__(self, msg):
        self.message = msg
        pass

    def __str__(self):
        return self.message


class Action(object):
    def __init__(self):
        pass

    def execute_sys_command(self, command, pwd=None, timeout=5):
        """
        Execute system command for action setting
        :param command: execute command
        :param pwd: set running path
        :param timeout: set running timeout
        :return: process id, process status code, standard stream output , standard error output
        """
        child = subprocess.Popen(command,
                                 shell=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 cwd=pwd,
                                 universal_newlines=True)
        start_time = time.clock()
        child_pid = child.pid
        while True:
            if child.poll() is not None:
                break
            time.sleep(1)
            if time.clock() - start_time > timeout:
                raise CommandTimeoutError("Execute command %s timeout %d" % (command, timeout))
        stdout, stderr = child.communicate()
        return child_pid, child.returncode, stdout, stderr

    def action(self, *args, **kwargs):
        pass


class SnmpTrapAction(Action):
    def __init__(self):
        pass

    def action(self, *args, **kwargs):
        command = "snmptrap -v %s -c %s %s 'master' %s %s s " \
                  "'%s'"
        version = kwargs['version']
        community = kwargs['community']
        oid = kwargs['oid']
        message = kwargs['message']
        snmp_trap = command % (version, community, ActionConstants.DEFAULT_ENTERPRISE_OID,
                               ActionConstants.SNMP_TARGET_SERVER, oid, message)
        pid, error_code, output, error_output = self.execute_sys_command(snmp_trap)
        return output


class ScriptAction(Action):
    def __init__(self):
        pass

    def action(self, *args, **kwargs):
        command = kwargs['command']
        pid, error_code, output, error_output = self.execute_sys_command(command)
        return output


class RundeckAction(Action):
    def __init__(self):
        pass

if __name__ == "__main__":
    pass
    # SnmpTrapAction().action()
    # action = SnmpTrapAction()
    # print action.execute_sys_command("ipconfig")
    # print ActionConstants.BASE_SCRIPT_PATH