__author__ = 'zhutong'

"""
A very simple session/cache manager for testing
Should be implemented using redis
"""

from threading import Thread
import time
from helper import get_logger
import Queue


class SessionManager(Thread):
    data_set = {}

    parser_dict={}

    polling_interval = 1
    absolute_timeout = 3600
    after_read_timeout = 300
    def __init__(self,zmq_publish):
        Thread.__init__(self)
        self.zmq_publish = zmq_publish

    def put(self, k, v):
        self.data_set[k] = v

    def update_device(self,task_id,device_info):
        try:
            self.data_set[task_id].update(dict(device_info=device_info))
        except KeyError:
            pass


    def update(self, k, v):
        try:
            self.data_set[k].update(v)
        except KeyError:
            pass
    def init_parser_queue(self,task_id):
        self.parser_dict[task_id] = Queue.Queue()

    def set_parser_queue(self,task_id,value):

        #data = self.data_set.get(task_id)
        #if "parser_queue" not in data:
        #data.update(dict(parser_queue=Queue.Queue(),parser_status="queue"))
        queue = self.parser_dict[task_id]
        queue.put(value)
        #data["parser_queue"].append(value)



    def update_command_result(self,task_id,result):
        data = self.data_set.get(task_id)
        
        channel = data["channel"]
        if "element_result" not in data:
                data.update(dict(element_result={}))

        if channel == "cli":
            command = result["command"]
            data.get("element_result")[command] = result
        else:
            clock = result["clock"]
            data.get("element_result")[clock] = result


    def update_parser_result(self,task_id,result):
        data = self.data_set.get(task_id)
        if "parser_result" not in data:
            data.update(dict(parser_result=[]))

        data.get("parser_result").append(result)
        
        data["parser_status"] = "queue"


    def get(self, k):
        data = self.data_set.get(k)
        #if data:
        #    data['timer'] = time.time()
        #    data['read'] = True
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
        while True:
            #time.sleep(self.polling_interval)
            time.sleep(self.polling_interval)
            for k in self.data_set.keys():
                v = self.data_set[k]
                status = v["status"] 
                if k in self.parser_dict:
                    parser_queue = self.parser_dict[k]
                    if v["parser_status"] == "queue":
                        if not parser_queue.empty():
                            data = parser_queue.get()
                            v["parser_status"]="runnning"
                            self.zmq_publish.send_string(data["publish_string"])
                        
                        if status == "coll_finish" and parser_queue.empty() and v["parser_status"] != "running":
                            v["status"] = "all_finish"
                            v["timer"] = time.time()
                
                if v["status"] == "all_finish" and time.time() - v['timer'] > self.after_read_timeout:
                    del self.data_set[k]
                    if k in self.parser_dict:
                        del self.parser_dict[k]
                    logger.info('Task %s timeout, cleared' % k)
            






