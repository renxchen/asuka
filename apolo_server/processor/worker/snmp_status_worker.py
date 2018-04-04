# __author__ = 'zhutong'

import sys
from worker_base import WorkerBase, main
from snmp_helper import SNMP,chunks
import json
import time
import traceback

class SNMPStatusWorker(WorkerBase):
    name = 'SNMP_status_check'
    channels = ('status_snmp',)
    threads = 5

    def handler(self, task_id, task,data, logger):
        device_info = task['device_info']
        ip = device_info['ip']
        community = device_info['community']
        snmp_model = device_info['snmp_model'] if "snmp_model" in device_info else 1
        is_translate = False
        device_log_info = "Device ID: %s,IP: %s,HostName: %s" % (device_info["device_id"],ip,device_info["hostname"])
        #sysObjectID
        status_check_oid = "1.3.6.1.2.1.1.2.0"

        logger.info('%s SNMP Status Check start' % device_log_info)
        worker = SNMP(ip,
                      community,
                      logger=logger,
                      port=device_info.get('port', 161),
                      timeout=device_info.get("timeout",5),
                      retries=device_info.get('retries', 2),
                      device_log_info=device_log_info,
                      model_version=snmp_model,
                      is_translate=is_translate
                      )
        try:

            result = worker.bulk_get([status_check_oid])
            result = result["output"][0]
            
            status = result["status"]
            message = result["message"]

        except Exception as e:            
            status = 'fail'
            message = str(e)
            logger.error("%s %s"%(device_log_info, str(e)))
            print traceback.format_exc()

        logger.info('%s SNMP Collection Finished' % device_log_info)

        result = dict(task_id=task_id,
             status=status,
             message=message,
             device_id=device_info['device_id'],
             result_type=self.channels[0]
            )

        return result


main(SNMPStatusWorker)
