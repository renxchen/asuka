import logging
import requests
import json
import time
from multiprocessing.dummy import Pool as ThreadPool
TIMEOUT = 60
DEFAULT_LOG_FILE_PATH = "log.log"
DEFAULT_LOG_LEVEL = logging.INFO
BASE_CLI_METHOD = "telnet"
BASE_CLI_PLATFORM = 'ios'
BASE_SNMP_METHOD = "bulk_get"
CLI_TYPE_CODE = 0
SNMP_TYPE_CODE = 1
CLI_THREADPOOL_SIZE = 150
SNMP_THREADPOOL_SIZE = 15
GET_CLI_DATA_SERVICE_URL = 'http://10.71.244.134:8080/api/v1/sync/%s'
GET_SNMP_DATA_SERVICE_URL = 'http://10.71.244.134:8080/api/v1/sync/%s'
GET_DEVICES_SERVICE_URL = "http://10.71.244.134:7777/api/v1/getCollectionInfor"
PARSER_SERVICE_URL = "http://10.71.244.134:7777/api/v1/parser"
TRIGGER_SERVICE_URL = "http://10.71.244.134:7777/api/v1/trigger"
# TRIGGER_SERVICE_URL = "http://127.0.0.1:8888/api/v1/trigger"


class LogMessage(object):
    DEBUG_NO_DEVICE_RUNNING_AT_TIME = "No device need to running"
    CRITICAL_SERVICE_TIMEOUT = "Wait Service response timeout"
    CRITICAL_SERVICE_CONNECT_ERROR = "Connect Service Error"

    CRITICAL_GET_DEVICE_INFORMATION_ERROR = "Get device information fail: %s"
    CRITICAL_COLLECTION_ERROR = "Collection fail: %s"
    CRITICAL_PARSER_ERROR = "Parser fail: %s"
    ERROR_COLLECTION = "Device %s collection fail: %s"
    ERROR_TRIGGER = "Trigger fail: %s"


class DeviceServiceExceptions(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class CollectionServiceException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ParserServiceException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class TriggerServiceException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def log_factory(**kwargs):
    # log_level = kwargs.get("log_level") if kwargs.get("log_level") else logging.WARNING
    log_level = DEFAULT_LOG_LEVEL
    logger = logging.getLogger(kwargs.get('log_name') if kwargs.get('log_name') else "root")
    logger.setLevel(log_level)
    fh = logging.FileHandler(DEFAULT_LOG_FILE_PATH)
    fh.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_devices(param):
    __service_url = GET_DEVICES_SERVICE_URL
    try:
        res = requests.post(__service_url, data=json.dumps(param), timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise DeviceServiceExceptions(LogMessage.CRITICAL_SERVICE_CONNECT_ERROR)
    except requests.exceptions.ReadTimeout:
        raise DeviceServiceExceptions(LogMessage.CRITICAL_SERVICE_TIMEOUT)
    status_code = res.status_code
    if status_code == 200:
        devices = json.loads(str(res.text))
    else:
        raise TriggerServiceException(str(res.text))
    if devices['status'] != "success":
        raise TriggerServiceException(LogMessage.CRITICAL_GET_DEVICE_INFORMATION_ERROR % devices['message'])
    return devices


def send_trigger(param):
    __service_url = TRIGGER_SERVICE_URL
    try:
        res = requests.post(__service_url, data=json.dumps(param), timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise TriggerServiceException(LogMessage.CRITICAL_SERVICE_CONNECT_ERROR)
    except requests.exceptions.ReadTimeout:
        raise TriggerServiceException(LogMessage.CRITICAL_SERVICE_TIMEOUT)
    status_code = res.status_code
    if status_code == 200:
        devices = json.loads(str(res.text))
    else:
        raise TriggerServiceException(str(res.text))
    if devices['status'] != "success":
        raise TriggerServiceException(LogMessage.ERROR_TRIGGER % devices['message'])
    return


def __get_cli_data(param):
    __base_url = GET_CLI_DATA_SERVICE_URL
    __url = __base_url % 'cli'
    try:
        res = requests.post(__url, data=json.dumps(param), timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise DeviceServiceExceptions(LogMessage.CRITICAL_SERVICE_CONNECT_ERROR)
    except requests.exceptions.ReadTimeout:
        raise DeviceServiceExceptions(LogMessage.CRITICAL_SERVICE_TIMEOUT)
    status_code = res.status_code
    if status_code == 200:
        output = json.loads(res.text)
    else:
        raise CollectionServiceException(LogMessage.CRITICAL_COLLECTION_ERROR % str(res.text))
    if output['status'] != "success":
        cli_collection_logger.error(LogMessage.ERROR_COLLECTION % (str(output['ip']), str(output['message'])))
        return
    try:
        send_handler_request_cli(param, output)
    except Exception, e:
        raise ParserServiceException(str(e))

    # try:
    #     send_trigger(param)
    # except Exception, e:
    #     raise TriggerServiceException(str(e))

    return output


def send_handler_request_cli(param, output):
    __service_url = PARSER_SERVICE_URL
    param['start_time'] = output.get('start_time')
    param['end_time'] = output.get('end_time')
    param['item_type'] = CLI_TYPE_CODE
    tmp_dict = {}
    for output in output.get('output'):
        tmp_dict[str(output.get('command')).strip()] = output.get('output')
    for item in param['items']:
        item['output'] = tmp_dict[str(item['command']).strip()]
    try:
        res = requests.post(__service_url, data=json.dumps(param), timeout=TIMEOUT)
    except Exception:
        raise ParserServiceException(LogMessage.CRITICAL_SERVICE_TIMEOUT)
    status_code = res.status_code
    if status_code == 200:
        response = json.loads(str(res.text))
    else:
        raise ParserServiceException(str(res.text))
    if response['status'] != "success":
        raise ParserServiceException(LogMessage.CRITICAL_PARSER_ERROR % response['message'])


def cli_main():
    now_time = int(time.time())

    def __add_param(device={}):
        device.update(
            {
                "method": BASE_CLI_METHOD,
                "platform": BASE_CLI_PLATFORM,
                "task_timestamp": now_time
            }
        )
        return device
    devices = []
    cli_logger.info("Cli Task %d Begin" % now_time)
    param = dict(
        now_time=now_time,
        item_type=CLI_TYPE_CODE
    )
    devices = get_devices(param)
    items = []
    for i in devices['devices']:
        items.extend(i['items'])
    # send_trigger({"items": items, "task_timestamp": 123})
    try:
        devices = get_devices(param)
        devices = map(__add_param, devices['devices'])
        if len(devices) == 0:
            cli_logger.debug(LogMessage.DEBUG_NO_DEVICE_RUNNING_AT_TIME)
        pool = ThreadPool(CLI_THREADPOOL_SIZE)
        pool.map(__get_cli_data, devices)
        pool.close()
        pool.join()
    except DeviceServiceExceptions, e:
        cli_device_logger.error(str(e))
    except CollectionServiceException, e:
        cli_collection_logger.error(str(e))
    except ParserServiceException, e:
        cli_parser_logger.error(str(e))
    except TriggerServiceException, e:
        cli_trigger_logger.error(str(e))
    except Exception, e:
        cli_logger.error(str(e))
    cli_logger.info("Cli Task %d End" % now_time)
    cli_logger.info("Total device task: %d" % len(devices))


def __get_snmp_data(param):
    __base_url = GET_SNMP_DATA_SERVICE_URL
    __url = __base_url % 'snmp'
    try:
        res = requests.post(__url, data=json.dumps(param), timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise DeviceServiceExceptions(LogMessage.CRITICAL_SERVICE_CONNECT_ERROR)
    except requests.exceptions.ReadTimeout:
        raise DeviceServiceExceptions(LogMessage.CRITICAL_SERVICE_TIMEOUT)
    status_code = res.status_code
    if status_code == 200:
        output = json.loads(res.text)
    else:
        raise CollectionServiceException(LogMessage.CRITICAL_COLLECTION_ERROR % str(res.text))
    send_handler_request_snmp(param, output)
    return output


def send_handler_request_snmp(param, output):
    __service_url = PARSER_SERVICE_URL
    param['start_time'] = output.get('start_time')
    param['end_time'] = output.get('end_time')
    param['item_type'] = SNMP_TYPE_CODE

    tmp_dict = {}
    for output in output['output']:
        tmp_dict[str(output['oid']).strip()] = output['output']
    for item in param['items']:
        item['output'] = tmp_dict[str(item['oid']).strip()]
    try:
        res = requests.post(__service_url, data=json.dumps(param), timeout=TIMEOUT)
    except Exception:
        raise ParserServiceException(LogMessage.CRITICAL_SERVICE_TIMEOUT)
    status_code = res.status_code
    if status_code == 200:
        response = json.loads(str(res.text))
    else:
        raise ParserServiceException(str(res.text))
    if response['status'] != "success":
        raise ParserServiceException(LogMessage.CRITICAL_PARSER_ERROR % response['message'])


def snmp_main():
    now_time = int(time.time())

    def __add_param(device={}):
        device.update(
            {
                "task_timestamp": now_time
            }
        )
        return device
    snmp_logger.info("Snmp Task %d Begin" % now_time)
    param = dict(
        now_time=now_time,
        item_type=SNMP_TYPE_CODE
    )
    devices = []
    try:
        devices = get_devices(param)
        devices = map(__add_param, devices['devices'])
        if len(devices) == 0:
            snmp_logger.debug(LogMessage.DEBUG_NO_DEVICE_RUNNING_AT_TIME)
        pool = ThreadPool(SNMP_THREADPOOL_SIZE)
        pool.map(__get_snmp_data, devices)
        pool.close()
        pool.join()
    except DeviceServiceExceptions, e:
        snmp_device_logger.error(str(e))
    except CollectionServiceException, e:
        snmp_collection_logger.error(str(e))
    except ParserServiceException, e:
        snmp_parser_logger.error(str(e))
    except TriggerServiceException, e:
        snmp_trigger_logger.error(str(e))
    except Exception, e:
        snmp_logger.error(str(e))
    snmp_logger.info("Snmp Task %d End" % now_time)
    snmp_logger.info("Total device task: %d" % len(devices))


if __name__ == "__main__":
    now_time = int(time.time())
    snmp_parser_logger = log_factory(log_name="Snmp_Parser")
    snmp_collection_logger = log_factory(log_name="Snmp_Collection")
    snmp_device_logger = log_factory(log_name="Snmp_Device")
    snmp_trigger_logger = log_factory(log_name="Snmp_Trigger")
    snmp_logger = log_factory(log_name="Snmp")
    cli_parser_logger = log_factory(log_name="Cli_Parser")
    cli_collection_logger = log_factory(log_name="Cli_Collection")
    cli_device_logger = log_factory(log_name="Cli_Device")
    cli_trigger_logger = log_factory(log_name="Cli_Trigger")
    cli_logger = log_factory(log_name="Cli")
    cli_main()
    # snmp_main()
    end_time = int(time.time())
    print end_time - now_time
