# -*- coding: utf-8 -*-
import json
import logging
import os
import time
import zmq
import threading
from threading import Thread
from Pantheon.Venus.configurations import Configurations
from tornado import options
from Pantheon.Venus.helper import get_logger

__author__ = 'Zhu Tong <zhtong@cisco.com>'
__version__ = '0.5'


counter_lock = threading.Lock()


class WorkerBase(Thread):
    channels = []

    def __init__(self, name, server, ports):
        Thread.__init__(self)
        self.name = name
        self.logger = get_logger(name, logging.INFO)
        self.server = server
        self.ports = ports

    def run(self):
        logger = self.logger

        context = zmq.Context()
        # zmq socket 用来接收服务器发送的新任务通知
        zmq_subscripe = context.socket(zmq.SUB)
        zmq_subscripe.connect("tcp://%s:%s" % (self.server, self.ports[0]))
        for channel in self.channels:
            zmq_subscripe.setsockopt(zmq.SUBSCRIBE, channel)
        # zmq socket 用来向server取任务
        zmq_reqest = context.socket(zmq.REQ)
        zmq_reqest.setsockopt(zmq.RCVTIMEO, 3600000)
        zmq_reqest.connect("tcp://%s:%s" % (self.server, self.ports[1]))
        # zmq socket 用来推送结果给server
        zmq_push = context.socket(zmq.PUSH)
        zmq_push.connect("tcp://%s:%s" % (self.server, self.ports[2]))

        logger.info('Worker started')
        while True:
            try:
                # waiting for command from server
                channel, message = zmq_subscripe.recv_string().split()
                logger.debug('Receive published message: %s', message)
                if message == 'task':  # has new task
                    logger.debug('Request for task')
                    # request new task
                    zmq_reqest.send_string(b'%s' % channel)
                    task_id, task_str = zmq_reqest.recv().split(' ', 1)
                    logger.info('Task started: %s', task_id)
                    # deal with task by handler, and get result
                    task = json.loads(task_str)
                    start_time = time.strftime('%Y-%m-%d %H:%M:%S')
                    global counter_loc
                    if counter_lock.acquire():
                        result = self.handler(task_id, task, logger)
                        counter_lock.release()
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S')
                    result.update(dict(start_time=start_time, end_time=end_time))
                    # push result to server
                    zmq_push.send(json.dumps(result))
                    del result
                    logger.info('Task finished: %s', task_id)
            except ValueError:
                pass
            except zmq.Again:
                logger.error('Again')
                pass
            except zmq.ZMQError:
                logger.error('ZMQ Error')
                pass

    def handler(self, task_id, task, logger):
        pass


def main(worker):
    options.define("s", default='localhost', help="zmq server", type=str)
    options.define("t", default=10, help="threads", type=int)
    options.parse_command_line()
    server = options.options.s
    threads = options.options.t
    if hasattr(worker, "threads"):
        threads = worker.threads

    pid = os.getpid()
    config = Configurations()
    ports = (str(config.get_configuration("zmqPublish")),
             str(config.get_configuration("zmqDispatch")),
             str(config.get_configuration("zmqResult")))
    for tid in range(threads):
        worker_name = '%s-%05d-%04d' % (worker.name, pid, tid)
        work = worker(worker_name, server, ports)
        work.daemon = True
        work.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
