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
    threads = 1
    default_timeout = 5
    default_retries = 2

    def handler(self, task_id, task,data, logger):
        device_info = task['device_info']
        ip = device_info['ip']
        community = device_info['community']
        snmp_model = 0 if device_info.get("snmp_version","").upper() == "V1" else 1
        is_translate = False
        device_id = device_info.get("device_id","")
        device_log_info = "Device ID: %s,IP: %s,HostName: %s" % (device_id,ip,device_info["hostname"])
        #sysObjectID
        status_check_oid = "SNMPv2-MIB::sysObjectID.0"

        logger.info('%s SNMP Status Check start' % device_log_info)
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

            result = worker.bulk_get([status_check_oid])
            result = result["output"][0]
            
            status = result["status"]
            message = result["message"]

        except Exception as e:            
            status = 'fail'
            message = str(e)
            logger.error("%s %s"%(device_log_info, str(e)))
            print traceback.format_exc()

        logger.info('%s SNMP Status Check Finished' % device_log_info)

        result = dict(task_id=task_id,
             status=status,
             message=message,
             device_id=device_id,
             result_type=self.channels[0]
            )

        return result


main(SNMPStatusWorker)
