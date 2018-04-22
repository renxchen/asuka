__author__ = 'zhutong'

"""
A very simple session/cache manager for testing
Should be implemented using redis
"""
import threading
#from threading import Thread
import time
from helper import get_logger
import Queue


class SessionManager(threading.Thread):
    data_set = {}
    mutux_dict={}

    polling_interval = 60
    absolute_timeout = 10*60
    after_finish_timeout = 60
    mutux_after_finish_timeout = 60*60

    parser_queue = Queue.Queue()
    def __init__(self,handle_pedding_task_func):
        threading.Thread.__init__(self)
        self.pedding_fuc = handle_pedding_task_func

    def put(self, k, v):
        self.data_set[k] = v

    def update_device(self,task_id,device_info):
        try:
            self.data_set[task_id]["device_info"].update(device_info)
        except KeyError:
            pass

    def get_threading_lock(self,device_id):
        if device_id in self.mutux_dict:
            self.mutux_dict[device_id]["timer"] = None
            return self.mutux_dict[device_id]["mutex"]
        else:
            mutex = threading.Lock()
            self.mutux_dict[device_id] = {
                "timer":None,
                "mutex":mutex
            }
            return mutex

    def set_lock_timer(self,device_id):
        if device_id in self.mutux_dict:
            self.mutux_dict[device_id]["timer"] = time.time()

    def update(self, k, v):
        try:
            self.data_set[k].update(v)
        except KeyError:
            pass

    def update_parser_result(self,task_id,result):
        data = self.data_set.get(task_id)
        clock = result["collection_clock"]
        data.setdefault("parser_result",{})[clock] = result
        

    def get(self, k):
        data = self.data_set.get(k)
        return data

    def set_read(self, k):
        data = self.data_set.get(k)
        if data:
            data['timer'] = time.time()
            data['read'] = True

    def get_all(self):
        return self.data_set

    def get_timer(self):
        return dict(polling_interval=self.polling_interval,
                    absolute_timeout=self.absolute_timeout,
                    after_read_timeout=self.after_read_timeout)

    def set_timer(self,
                  polling_interval,
                  absolute_timeout,
                  after_read_timeout):
        try:
            polling_interval = int(polling_interval)
            absolute_timeout = int(absolute_timeout)
            after_read_timeout = int(after_read_timeout)
            if absolute_timeout >= 300:
                self.absolute_timeout = absolute_timeout
            if after_read_timeout >= 30:
                self.after_read_timeout = after_read_timeout
            if polling_interval >= 1:
                self.polling_interval = polling_interval
        except ValueError:
            pass

    def run(self):
        logger = get_logger('SessionMgr')
        threading_lock_interval_counter = 0
        while True:
            threading_lock_interval_counter += 1 
            time.sleep(self.polling_interval)
            for k in self.data_set.keys():
                v = self.data_set[k]
                status = v["status"]   
                now = time.time()

                if (now - v['timer']) > self.absolute_timeout:
                    try:
                        channel = v["channel"]
                        if channel in "cli snmp":
                            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                            device_id = v["device_info"]["device_id"]
                            self.pedding_fuc(channel,device_id,now,timestamp)
                        del self.data_set[k]
                        logger.info('Task %s Timeout, cleared' % k)
                    except Exception,e:
                        logger.error(str(e))

                elif "finish_timer" in v and (now - v['finish_timer']) > self.after_finish_timeout:
                    del self.data_set[k]
                    logger.info('Task %s Finished, cleared' % k)
            
            if threading_lock_interval_counter == 60:
                threading_lock_interval_counter = 0
                for k in self.mutux_dict.keys():
                    if k in self.mutux_dict:
                        timer = self.mutux_dict[k]["timer"]
                        if timer and (time.time() - timer > self.mutux_after_finish_timeout):
                            del self.mutux_dict[k]
                            logger.info('Device:%s Mutex timeout, cleared' % k)
