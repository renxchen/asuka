import requests
import time
import json
from optparse import OptionParser
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
        print json.dumps(res.text, indent=2)
    except Exception, e:
        print str(e)
    print "Task End"

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-t', '--type', dest="type", help="cli or snmp", default="cli")
    (options, args) = parser.parse_args()
    s_type = options.type
    # print s_type
    collector(s_type)
    # collection('cli')


