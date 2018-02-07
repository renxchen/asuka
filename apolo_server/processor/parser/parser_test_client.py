from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import time

def __parser(data):
    __service_url =  "http://127.0.0.1:7777/api/v1/parser"
    res = requests.post(__service_url, data=json.dumps(data), timeout=30)


def main():
    with open("test_cli_param.json") as f:
        test_cli_param = json.loads(f.read())
    data = []
    for i in range(1):
        data.append(test_cli_param)
    pool = ThreadPool(20)
    pool.map(__parser, data)
    pool.close()
    pool.join()

if __name__ == "__main__":
    time.clock()
    main()
    print time.clock()