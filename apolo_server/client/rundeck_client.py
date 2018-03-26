import requests
import time
import json
BASE_CLI_URL = "http://127.0.0.1:7777/api/v1/sync/cli"
BASE_SNMP_URL = "http://127.0.0.1:7777/api/v1/sync/snmp"


def collector(collection_type):
    print "Task Start"
    if collection_type == 'cli':
        url = BASE_CLI_URL
    else:
        url = BASE_SNMP_URL
    now_time = int(time.time())
    param = {"now_time": now_time}
    try:
        res = requests.post(url, param)
    except Exception, e:
        print str(e)
    print json.dumps(res.text, indent=2)
    print "Task End"

if __name__ == "__main__":
    collector('snmp')
    # collection('cli')


