import requests
import json
import time
from multiprocessing.dummy import Pool as ThreadPool
BASE_CLI_METHOD = "telnet"
BASE_CLI_PLATFORM = 'ios'
BASE_SNMP_METHOD = "get"
CLI_TYPE_CODE = 0
SNMP_TYPE_CODE = 1


class DeviceExceptions(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class CollectionException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def __add_param(device={}):
    device.update(
        {
            "method": BASE_CLI_METHOD,
            "platform": BASE_CLI_PLATFORM,
            "operate": BASE_SNMP_METHOD
        }
    )
    return device


def get_devices(time_stamp, policy_type):
    __service_url = "http://127.0.0.1:8888/api/v1/getCollectionInfor"
    param = dict(
        now_time=time_stamp,
        item_type=policy_type
    )
    res = requests.post(__service_url, data=json.dumps(param))
    status_code = res.status_code
    if status_code == 200:
        devices = json.loads(str(res.text))
    else:
        raise DeviceExceptions(str(res.text))
    if devices['status'] != "success":
        raise DeviceExceptions("Get Devices information Error:%s" % devices['message'])
    return map(__add_param, devices['output'])


def __get_cli_data(param):
    __base_url = 'http://10.71.244.134:8080/api/v1/sync/%s'
    output = []
    __url = __base_url % 'cli'
    res = requests.post(__url, data=json.dumps(param))
    status_code = res.status_code
    # print res.text
    if status_code == 200:
        output = res.text
    else:
        raise CollectionException("Collection Error:%s" % str(res.text))
    print output
    return output


def __get_snmp_data(param):
    __base_url = 'http://10.71.244.134:8080/api/v1/sync/%s'
    __url = __base_url % 'snmp'
    res = requests.post(__url, data=json.dumps(param))
    status_code = res.status_code
    if status_code == 200:
        output = res.text
    else:
        raise CollectionException("Collection Error:%s" % str(res.text))

    return output


def cli_main():
    now_time = int(time.time())
    devices = get_devices(now_time, CLI_TYPE_CODE)
    pool = ThreadPool(15)
    pool.map(__get_cli_data, devices)
    pool.close()
    pool.join()


if __name__ == "__main__":
    cli_main()