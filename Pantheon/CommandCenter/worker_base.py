# -*- coding: utf-8 -*-

__author__ = 'Zhu Tong <zhtong@cisco.com>'
__version__ = '0.5'

import json
import logging
import os
import time
from threading import Thread

import zmq
from tornado import options

from helper import get_logger


class WorkerBase(Thread):
    channels = []

    def __init__(self, name, server):
        Thread.__init__(self)
        self.name = name
        self.logger = get_logger(name, logging.INFO)
        self.server = server

    def run(self):
        logger = self.logger
        context = zmq.Context()
        # zmq socket 用来接收服务器发送的新任务通知
        zmq_subscripe = context.socket(zmq.SUB)
        zmq_subscripe.connect("tcp://%s:6000" % self.server)
        for channel in self.channels:
            zmq_subscripe.setsockopt(zmq.SUBSCRIBE, channel)
        # zmq socket 用来向server取任务
        zmq_reqest = context.socket(zmq.REQ)
        zmq_reqest.setsockopt(zmq.RCVTIMEO, 3600000)
        zmq_reqest.connect("tcp://%s:6001" % self.server)
        # zmq socket 用来推送结果给server
        zmq_push = context.socket(zmq.PUSH)
        zmq_push.connect("tcp://%s:6002" % self.server)

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
                    result = self.handler(task_id, task, logger)
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
    options.define("t", default=5, help="threads", type=int)
    options.parse_command_line()
    server = options.options.s
    threads = options.options.t

    pid = os.getpid()
    for tid in range(threads):
        worker_name = '%s-%05d-%04d' % (worker.name, pid, tid)
        work = worker(worker_name, server)
        work.daemon = True
        work.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

