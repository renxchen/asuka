# __author__ = 'zhutong'

import sys
from worker_base import WorkerBase, main
from snmp_helper import SNMP,chunks
import json
import time

class SNMPWorker(WorkerBase):
    name = 'SNMP'
    channels = ('snmp',)
    threads = 1
    max_batch_vars = 20
    default_timeout = 5
    default_retries = 2

    def handler(self, task_id, task,data, logger):
        device_info = task['device_info']
        ip = device_info['ip']
        community = device_info['community']
        snmp_model = 0 if device_info.get("snmp_version","").upper() == "V1" else 1
        is_translate = False
        device_id = device_info.get("device_id","")
        device_log_info = "Device ID:%s, IP:%s, HostName: %s" % (device_id, ip, device_info["hostname"])
      
        oids=[]
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

        logger.info('%s SNMP Collection Start' % device_log_info)
        worker = SNMP(ip,
                      community,
                      logger=logger,
                      port=device_info.get('port', 161),
                      timeout=device_info.get("timeout",self.default_timeout),
                      retries=device_info.get('retries', self.default_retries),
                      device_log_info=device_log_info,
                      model_version=snmp_model,
                      is_translate=is_translate
                      )
        try:
                       
            if len(oids) > self.max_batch_vars:
                _oid_splits = chunks(oids, self.max_batch_vars)
            else:
                _oid_splits = [oids]

            for _oids in _oid_splits:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                clock = time.time()
                result = worker.bulk_get(_oids)
                
                for data in result["output"]:
                    data["item_ids"] = oid_dict[data["origin_oid"]]
                
                result.update(dict(result_type="element_result", task_id=task_id, timestamp=timestamp, clock="%f" % clock))
                self.zmq_push.send(json.dumps(result))
                
            status = "success"
            message = ""
        except Exception as e:            
            status = 'fail'
            message = str(e)
            logger.error("%s %s"%(device_log_info, str(e)))

        logger.info('%s SNMP Collection Finished' % device_log_info)

        result = dict(task_id=task_id,
             status=status,
             message=message,
             result_type="task_result",
             device_id=device_id
            )

        return result


main(SNMPWorker)
