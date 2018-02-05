import multiprocessing
import sys

from snmp_worker import SNMPWorker
from cisco_cli_worker import CiscoCliWorker
from worker_base import main


def worker(worker_type):
    if worker_type == "snmp":
        main(SNMPWorker)
    else:
        main(CiscoCliWorker)

if __name__ == "__main__":
    worker_type = sys.argv[1]
    process_num = sys.argv[2]
    processes = []
    for i in range(0, int(process_num)):
        # print i
        p = multiprocessing.Process(target=worker, args=(worker_type,))
        processes.append(p)
    for i in processes:
        i.start()
    for i in processes:
        i.join()
