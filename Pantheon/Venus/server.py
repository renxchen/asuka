# -*- coding: utf-8 -*-
from tornado import web, ioloop, options
from configurations import Configurations
from units import save_output_file
from zmq.eventloop.ioloop import ZMQIOLoop
from zmq.eventloop.zmqstream import ZMQStream
from threading import Thread
from session_mgr import SessionManager
# from collection.collection_help import get_collection_devices, get_items
from collection.collection_helper import get_devices, get_valid_items
import json
import time
import threading
import os
import Queue
import zmq
import logging
import uuid
__author__ = 'Rubick <haonchen@cisco.com>'
__version__ = '0.1'


class TaskDispatcher(Thread):
    """
    该线程通过zmq接收Worker的任务请求，从相应Channel的队列中读取队列，发给Worker
    """
    def run(self):
        while True:
            channel = zmq_dispatch.recv_string()  # got task request from worker
            q = task_q[channel]
            logging.debug('Receive request from %s worker' % channel)
            if q.qsize():
                task_id = q.get()
                task = session_mgr.get(task_id)
                session_mgr.update(task_id, dict(status='start'))
                zmq_dispatch.send_string(b'%s %s' % (task_id, json.dumps(task)))
                logging.debug('Sent task %s to %s worker' % (task_id, channel))
            else:
                zmq_dispatch.send_string(b'')


class TestApiHandler(web.RequestHandler):

    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write(json.dumps({"test": "test success"}))
        self.finish()

    def put(self, *args, **kwargs):
        try:
            self.set_header("Content-Type", "application/json")
            params = json.loads(self.request.body)
            print params
            self.write(json.dumps(
                "Success"
            ))
        except Exception, e:
            self.write(json.dumps(
                "Error"
            ))
        self.finish()


class CollectionApiHandle(web.RequestHandler):
    @web.asynchronous
    def post(self, *args, **kwargs):
        try:
            param = json.loads(self.request.body)
            now_time = param["now_time"]
            item_type = param["item_type"]
            # other_param = param["other_param"] if "other_param" in param else []
            devices_info = get_devices(now_time, item_type)

            result = dict(
                status="success",
                devices=devices_info,
                message=""
            )
        except Exception, e:
            result = dict(
                status="success",
                devices=[],
                message=str(e)
            )

        self.write(json.dumps(result))
        self.finish()



class ItemsApiHandle(web.RequestHandler):
    @web.asynchronous
    def post(self, *args, **kwargs):
        try:
            param = json.loads(self.request.body)
            now_time = param["now_time"]
            item_type = param["item_type"]
            # other_param = param["other_param"] if "other_param" in param else []
            items = get_valid_items(now_time, item_type)

            result = dict(
                status="success",
                items=items,
                message=""
            )
        except Exception, e:
            result = dict(
                status="success",
                items=[],
                message=str(e)
            )

        self.write(json.dumps(result))
        self.finish()


class ParserApiHandle(web.RequestHandler):
    @web.asynchronous
    def post(self, *args, **kwargs):
        def cb_func(response, *args):
            self.write(json.dumps(response, indent=2))
            self.finish()
            session_mgr.set_read(task_id)
            del task_dict[task_id]
        channel = "parser"
        self.set_header("Content-Type", "application/json")
        params = json.loads(self.request.body)
        task_id = uuid.uuid4().hex
        timer = time.time()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        session_mgr.put(task_id,
                        dict(status='Queue',
                             params=params,
                             timer=timer,
                             timestamp=timestamp,
                             read=False,
                             category=channel))
        if channel not in task_q:
            task_q[channel] = Queue.Queue()
        q = task_q[channel]
        q.put(task_id)
        task_dict[task_id] = cb_func, None
        zmq_publish.send_string(b'%s task' % channel)
        logging.info('Publish new task %s to %s' % (task_id, channel))


class TriggerApiHandle(web.RequestHandler):
    @web.asynchronous
    def post(self, *args, **kwargs):
        def cb_func(response, *args):
            self.write(json.dumps(response, indent=2))
            self.finish()
            session_mgr.set_read(task_id)
            del task_dict[task_id]
        channel = "trigger"
        self.set_header("Content-Type", "application/json")
        params = json.loads(self.request.body)
        task_id = uuid.uuid4().hex
        timer = time.time()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        session_mgr.put(task_id,
                        dict(status='Queue',
                             params=params,
                             timer=timer,
                             timestamp=timestamp,
                             read=False,
                             category=channel))
        if channel not in task_q:
            task_q[channel] = Queue.Queue()
        q = task_q[channel]
        q.put(task_id)
        task_dict[task_id] = cb_func, None
        zmq_publish.send_string(b'%s task' % channel)
        logging.info('Publish new task %s to %s' % (task_id, channel))


class SaveFileApiHandle(web.RequestHandler):
    def put(self, *args, **kwargs):
        message = {}
        try:
            self.set_header("Content-Type", "application/json")
            params = json.loads(self.request.body)
            # create new task
            task_id = uuid.uuid4().hex
            timer = time.time()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            if "fileType" not in params:
                channel = "cliSaveFile"
            else:
                channel = params['fileType']

            # channel = 'saveFile'
            session_mgr.put(task_id,
                            dict(status='Queue',
                                 params=params,
                                 timer=timer,
                                 timestamp=timestamp,
                                 read=False,
                                 category=channel))
            if channel not in task_q:
                task_q[channel] = Queue.Queue()
            q = task_q[channel]
            q.put(task_id)
            zmq_publish.send_string(b'%s task' % channel)
            logging.info('Publish new task %s to %s' % (task_id, channel))
        except Exception, e:
            message['status'] = "Error"
            message['message'] = str(e)
            self.write(
                json.dumps(
                    message
                )
            )
        self.finish()


def on_worker_data_in(data):
    result = json.loads(data[0])
    task_id = result['task_id']
    status = result['status']
    task = session_mgr.get(task_id)
    if task:
        timer = time.time()
        session_mgr.update(task_id, dict(status='finish',
                                         result=result,
                                         read=False,
                                         timer=timer))
    logging.info('Task %s done, status: %s' % (task_id, status))
    try:
        caller, arg = task_dict.get(task_id)
        Thread(target=caller, args=(result, arg)).start()
    except TypeError, e:
        pass


if __name__ == '__main__':
    options.define("p", default=7777, help="run on the given port", type=int)
    options.parse_command_line()
    config = Configurations()
    port = options.options.p

    loop = ZMQIOLoop()
    loop.install()
    context = zmq.Context()
    # zmq socket 用来通知workers有新任务
    zmq_publish = context.socket(zmq.PUB)
    zmq_publish.bind("tcp://127.0.0.1:%s" % str(config.get_configuration("zmqPublish")))
    # zmq socket 用来发送任务给Worker
    zmq_dispatch = context.socket(zmq.REP)
    zmq_dispatch.bind("tcp://127.0.0.1:%s" % str(config.get_configuration("zmqDispatch")))
    # zmq socket 用来接收Worker的任务结果
    zmq_result = context.socket(zmq.PULL)
    zmq_result.bind("tcp://127.0.0.1:%s" % str(config.get_configuration("zmqResult")))
    receiver = ZMQStream(zmq_result)
    receiver.on_recv(on_worker_data_in)

    task_dict = {}
    task_q = {}
    task_dispatcher = TaskDispatcher()
    task_dispatcher.daemon = True
    task_dispatcher.start()

    session_mgr = SessionManager()
    session_mgr.daemon = True
    session_mgr.start()

    print('Tornado server started on port %d' % port)
    print('Press "Ctrl+C" to exit.\n')
    web.Application([(r'/api/v1/test/?(.*)', TestApiHandler),
                     (r'/api/v1/saveOutput/?(.*)', SaveFileApiHandle),
                     (r'/api/v1/getCollectionInfor/?(.*)', CollectionApiHandle),
                     (r'/api/v1/parser/?(.*)', ParserApiHandle),
                     (r'/api/v1/trigger/?(.*)', TriggerApiHandle),
                     (r'/api/v1/getItems/?(.*)', ItemsApiHandle)
                     ],
                    autoreload=True,
                    ).listen(port)

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
