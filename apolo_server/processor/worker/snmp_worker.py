# __author__ = 'zhutong'

import sys
from ..constants import SYS_PATH
sys.path.append(SYS_PATH)
from snmp_helper import SNMP,chunks
from worker_base import WorkerBase, main
import json
import time

class SNMPWorker(WorkerBase):
    name = 'SNMP'
    channels = ('snmp',)
    threads = 1

    def handler(self, task_id, task,data, logger):
        device_info = task['device_info']

        ip = device_info['ip']
        community = device_info['community']
        commands = {}
        operate = 'bulk_get'
        snmp_model = device_info['snmp_model'] if "snmp_model" in device_info else 1
        is_translate = False if "is_translate" in device_info else True

        try:
            timeout = int(device_info["timeout"])
        except:
            timeout = 5

        oids=[]
        #items=[]
        oid_dict = {}
        for key in ["items_1day","items_1hour","items_15min","items_5min","items_1min"]:
            if key in device_info:
                for item in device_info[key]:
                    oid = item['oid']
                    item_id = item["item_id"]

                    if oid in oid_dict:
                        oid_dict[oid].append(item_id)
                    else:
                        oid_dict[oid] = [item_id]

                    if oid not in oids:
                        oids.append(oid)

   
        maxvars = 2

        logger.info('%s for %s started', operate.upper(), ip)
        worker = SNMP(ip,
                      community,
                      logger=logger,
                      port=commands.get('port', 161),
                      timeout=timeout,
                      retries=commands.get('retries', 2),
                      non_repeaters=commands.get('non_repeaters', 0),
                      max_repetitions=commands.get('max_repetitions', 25),
                      model_version=snmp_model,
                      is_translate=is_translate
                      )
        try:
            
            if operate == 'bulk_get':
                snmp_fun = worker.bulk_get
            else:
                return dict(task_id=task_id,
                            status='error',
                            message='Not support SNMP operate')
            
            
            if len(oids) > maxvars:
                _oid_splits = chunks(oids, maxvars)
            
            else:
                _oid_splits = [oids]

            for _oids in _oid_splits:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                clock = time.time()
                result = snmp_fun(_oids)
                
                for data in result["output"]:
                    data["item_ids"] = oid_dict[data["origin_oid"]]
                
                result.update(dict(result_type="element_result", task_id=task_id, timestamp=timestamp, clock="%f" % clock))
                self.zmq_push.send(json.dumps(result))


            logger.info('%s for %s finished', operate.upper(), ip)
            #result = snmp_fun(tuple(oids))
            status = "success"
            message = ""
        except Exception as e:            
            status = 'fail'
            message = str(e)

        result = dict(task_id=task_id,
             status=status,
             message=message,
             result_type="task_result",
             device_id=device_info['device_id']
            )

        return result


main(SNMPWorker)
