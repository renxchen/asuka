import subprocess
import time
import logging
import traceback
from apolo_server.processor.constants import ActionConstants
from apolo_server.processor.helper import get_logger
from apolo_server.processor.db_units.db_helper import ActionDbHelp
from login_helper import LoginServer

def _save_flow_log(func):
    def wrapper(cls, *args, **kwargs):
        cls.logger.debug("Begin %s, function: %s" % (cls.__class__, func.__name__))
        res = func(cls, *args, **kwargs)
        cls.logger.debug("End %s, function: %s" % (cls.__class__, func.__name__))
        return res
    return wrapper


def _save_exception_log(func):
    def wrapper(cls, *args, **kwargs):
        try:
            res = func(cls, *args, **kwargs)
            return res
        except Exception, e:
            traceback.print_exc()
            cls.logger.critical("Running Error: %s, please focus on %s, %s" % (e.message, cls.__class__, func.__name__))
            raise ActionError("Running Error: %s, please focus on %s, %s" % (e.message, cls.__class__, func.__name__))
        return None
    return wrapper


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
    def __init__(self, logger):
        self.test = "None"
        self.logger = logger
        pass

    @_save_exception_log
    def execute_sys_command(self, command, pwd=None, timeout=5):
        """
        Execute system command for action setting
        :param command: execute command
            str
        :param pwd: set running path
            str
        :param timeout: set running timeout
            int
        :return: process id, process status code, standard stream output , standard error output
        """
        self.logger.debug("Exec command: %s" % command)
        child = subprocess.Popen(command,
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 cwd=pwd,
                                 universal_newlines=True,
                                 bufsize=2048)
        start_time = time.clock()
        child_pid = child.pid
        while True:
            if child.poll() is not None:
                break
            time.sleep(1)
            if time.clock() - start_time > timeout:
                child.terminate()
                # raise CommandTimeoutError("Execute command %s timeout %d" % (command, timeout))
        stdout, stderr = child.communicate()
        return child_pid, child.returncode, stdout, stderr

    def alert(self, *args, **kwargs):
        pass

    @staticmethod
    def handle_error_output(pid, error_code, output, error_output):
        if error_code == 1:
            raise ActionError(output)

    @staticmethod
    def save_db_action_log(logs):
        ActionDbHelp.save_action_log(logs)


class SnmpTrapAction(Action):
    def __init__(self, logging):
        super(SnmpTrapAction, self).__init__(logging)
        pass

    @_save_flow_log
    @_save_exception_log
    def alert(self, *args, **kwargs):
        """
        version: str
                Snmp Version,
                e.g '1' or '2'
        community: str
        oid: str
        message: str
            It's content will be send to snmp trap server
        :param args:
        :param kwargs:
        :return: system reply message
        """
        command = "snmptrap -v %sc -c %s %s 'master' %s %s s '%s'"

        version = kwargs['version']
        community = kwargs['community']
        oid = kwargs['oid']
        message = kwargs['message']
        snmp_trap = command % (version, community, ActionConstants.DEFAULT_ENTERPRISE_OID,
                               ActionConstants.SNMP_TARGET_SERVER, oid, message)
        pid, error_code, output, error_output = self.execute_sys_command(snmp_trap)
        """
        if error code is 1, this code will raise error exception
        """
        # self.handle_error_output(pid, error_code, output, error_output)
        return output


class ScriptAction(Action):
    def __init__(self, logging):
        super(ScriptAction, self).__init__(logging)
        pass

    @_save_flow_log
    @_save_exception_log
    def alert(self, *args, **kwargs):
        command = kwargs['command']
        pid, error_code, output, error_output = self.execute_sys_command(command)
        return output


class RundeckAction(Action):
    def __init__(self, logging):
        super(RundeckAction, self).__init__(logging)
        pass

    @_save_exception_log
    def login_remote_exec_command(self, command):
        with LoginServer('10.79.148.106', 22, 'root', 'Cisco123') as p:
            result = p.exec_command(command)


def alert(action_information, logger):
    """
    :param action_information: dict
        action information
        dict's args:
                action_type: 0 or 1 or 2

                if action type is 0, it means that this action is snmptrap action. it still need below args:
                version: Snmp Version,
                    str
                    e.g '1' or '2'
                community:
                    str
                oid:
                    str
                message: str
                    It's content will be send to snmp trap server

                each alert need to be saved as log file which include:

                device_hostname:
                coll_policy:
                level: Critical/Major/Minor
                data: collected data

    :return:
    """
    action_type = action_information.get('action_type')
    device_hostname = action_information.get('device_hostname')
    coll_policy = action_information.get('coll_policy')
    level = action_information.get('level')
    data = action_information.get('data')
    action_id = action_information.get('action_id')
    args = {}
    if action_type == 0:
        args['version'] = action_information.get('version')
        args['community'] = action_information.get('community')
        args['oid'] = action_information.get('oid')
        args['message'] = action_information.get('message')
    elif action_type == 1:
        args['command'] = action_information.get('script_path')
    else:
        raise ActionError("Not support this action type")
    action_cls_name = ActionConstants.ACTION_TYPE_MAPPING.get(action_type)
    this_cls = __import__('action_helper')
    action_cls = getattr(this_cls, action_cls_name)
    action_instance = action_cls(logger)
    action_status = 0
    try:
        output = action_instance.alert(**args)
        action_status = 1
    except Exception, e:
        output = str(e)
    log = dict(
        device_hostname=device_hostname,
        action_time=time.time(),
        action_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        coll_policy_name=coll_policy,
        action_level=level,
        extra_data=data,
        action_status=action_status,
        exec_response=output,
        action_id=action_id,
        exec_action=action_type
    )
    ActionDbHelp.save_action_log([log])


if __name__ == "__main__":
    test = {
        'action_type': 0,
        'version': 2,
        'community': 'community',
        'oid': 'oid',
        'message': '123123123',
        'device_hostname': 'test',
        'coll_policy': 'test',
        'level': 0,
        'data': 'hahah',
        'action_id': 1,
        'script_path': "python C:\\Users\\haonchen\\Desktop\\print_t.py"
    }
    alert(test, get_logger('Action'))
    # SnmpTrapAction().action()
    # action = SnmpTrapAction()
    # print action.execute_sys_command("ipconfig /all")
    # print ActionConstants.BASE_SCRIPT_PATH