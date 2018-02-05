# __author__ = 'zhutong'

from snmp_helper import SNMP
# from snmp_helper import SNMP
from worker_base import WorkerBase, main


class SNMPWorker(WorkerBase):
    name = 'SNMP'
    channels = ('snmp',)
    threads = 1

    def handler(self, task_id, task, logger):
        device_info = task['device_info']
        ip = device_info['ip']
        community = device_info['community']
        commands = task['commands']
        operate = commands['operate']
        snmp_model = device_info['snmp_model'] if "snmp_model" in device_info else 1
        is_translate = False if "is_translate" in device_info else True
        # oids = [str(o).strip('.') for o in commands['oids']]
        oids = commands['oids']

        logger.info('%s for %s started', operate.upper(), ip)
        worker = SNMP(ip,
                      community,
                      logger=logger,
                      port=commands.get('port', 161),
                      timeout=commands.get('timeout', 5),
                      retries=commands.get('retries', 1),
                      non_repeaters=commands.get('non_repeaters', 0),
                      max_repetitions=commands.get('max_repetitions', 25),
                      model_version=snmp_model,
                      is_translate=is_translate
                      )
        try:
            if operate == 'get':
                snmp_fun = worker.get
            elif operate == 'walk':
                snmp_fun = worker.walk
            elif operate == 'bulk_walk':
                snmp_fun = worker.bulk_walk
            elif operate == 'get_multiple':
                snmp_fun = worker.get_multiple
            elif operate == 'bulk_get':
                snmp_fun = worker.bulk_get
            else:
                return dict(task_id=task_id,
                            status='error',
                            message='Not support SNMP operate')
            result = snmp_fun(oids)
            logger.info('%s for %s finished', operate.upper(), ip)
            # result = snmp_fun(tuple(oids))
        except Exception as e:
            return dict(task_id=task_id,
                        status='error',
                        message=str(e))

        result.update(task_id=task_id, ip=ip)
        return result


# main(SNMPWorker)
