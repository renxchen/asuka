# -*- coding: utf-8 -*-
__version__ = '0.1'
__author__ = 'Rubick <haonchen@cisco.com>'
import sys
import os
from constants import SYS_PATH
sys.path.append(SYS_PATH)
import json
import time
import Queue
import zmq
import logging
import uuid
from tornado import web, ioloop, options
from zmq.eventloop.ioloop import ZMQIOLoop
from zmq.eventloop.zmqstream import ZMQStream
from threading import Thread
from apolo_server.processor.session_mgr import SessionManager
from apolo_server.processor.configurations import Configurations
from apolo_server.processor.collection.devices_helper import get_devices

class TaskDispatcher(Thread):
    """
    Task Dispatcher
    """
    def run(self):
        while True:
            # got task request from worker
            result = zmq_dispatch.recv_string().split()  
            channel = result[0]
            task_id = None
            if len(result) == 2:
                task_id = result[1]
            
            logging.debug('Receive request from %s worker' % channel)
            if channel in "cli snmp":
                _device_q = device_q[channel]
                if _device_q.qsize():
                    device_task_dict = cli_device_task_dict if channel == "cli" else snmp_device_task_dict
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                    device_id = _device_q.get()
                    task_id = device_task_dict[device_id]
                    task = session_mgr.get(task_id)
                    session_mgr.update(task_id, dict(status='coll_start',coll_start_timestamp=timestamp))
                    zmq_dispatch.send_string(b'%s %s' % (task_id, json.dumps(task)))
                    logging.debug('Sent task %s to %s worker' % (task_id, channel))
            elif channel.startswith("parser"):
                if task_id:
                    task = session_mgr.get(task_id)
                    zmq_dispatch.send_string(b'%s %s' % (task_id, json.dumps(task)))
                    logging.debug('Sent task %s to %s worker' % (task_id, channel))
            else:
                zmq_dispatch.send_string(b'')

class CommandApiHandler(web.RequestHandler):
    @web.asynchronous
    def post(self, *args, **kwargs):
        
        self.set_header("Content-Type", "application/json")
        method = args[0]
        channel = args[1]

        # url should be valid
        if method != 'sync' or channel not in 'cli snmp':
            self.write(json.dumps(dict(status='error',
                                       message='Not support method')))
            self.finish()
            return

        #get device and deviceinfo
        devices,device_info_dict = get_devices(int(time.time()), channel)

        #get snmp or cli device q
        if channel not in device_q:
            device_q[channel] = Queue.Queue()
        _device_q = device_q[channel]

        #get pending dict and device_task dict 
        device_pending_dict = cli_device_pending_dict if channel == "cli" else snmp_device_pendding_dict
        device_task_dict = cli_device_task_dict if channel == "cli" else snmp_device_task_dict
        
        for device_id in devices:
            #get device info
            device_info = device_info_dict[device_id]
            if device_id in device_pending_dict:
                #update pending data
                device_pending_dict[device_id].update(device_info)
                continue

            #check device in device q
            if device_id in _device_q.queue:
                #get task by device id and update device_info
                task_id =  device_task_dict[device_id]
                task = session_mgr.get(task_id)
                if task["status"] == "coll_queue":
                    session_mgr.update_device(task_id,device_info)
                    continue
    
            if device_id in device_task_dict:
                task_id = device_task_dict[device_id]
                task = session_mgr.get(task_id)
                if task["status"] != "coll_queue":
                    device_pending_dict[device_id] = device_info
                    
            else:
                # create new task
                task_id = uuid.uuid4().hex
                device_task_dict[device_id] = task_id
                
                timer = time.time()
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                session_mgr.put(task_id,
                                dict(status='coll_queue',
                                    device_info=device_info,
                                    timer=timer,
                                    coll_queue_timestamp=timestamp,
                                    channel=channel,
                                    parser_status="queue"

                                    ))
                
                session_mgr.init_parser_queue(task_id)
                _device_q.put(device_id)

                # publish the new task to the channel
                zmq_publish.send_string(b'%s task' % channel)
                logging.info('Publish new task %s to %s' % (task_id, channel))

        result = dict(
            status="success",
            message="",
            devices=devices
        )
    
        self.write(json.dumps(result))
        self.finish()

def on_worker_data_in(data):
    
    result = json.loads(data[0])

    result_type = result['result_type']
    task_id = result['task_id']
    status = result['status']

    del result['result_type']
    del result['task_id']

    task = session_mgr.get(task_id)
    channel = task["channel"]
    if result_type == "element_result":
        print "enter command"
        session_mgr.update_command_result(task_id,result)


        new_channel = "parser"
        if channel == "snmp":
            find_key = result["clock"]
            #zmq_publish.send_string(b'%s task %s %s' % (new_channel,task_id,find_key))
        else:
            find_key = result["command"]
            #first_element = result["first_element"]
            #next_element = result["next_element"]
            
        session_mgr.set_parser_queue(task_id,dict(publish_string=b'%s task %s %s' % (new_channel,task_id,find_key)))

        logging.info('Collection element Task Done')

        #logging.info('Collection Task %s %s done, status: %s' % (task_id, status))
    elif result_type == "task_result":

        timer = time.time()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        session_mgr.update(task_id, dict(status='coll_finish',
                                         coll_finish_timestamp=timestamp,
                                         coll_result=result))
        
        device_id = result["device_id"]
        device_pending_dict = cli_device_pending_dict if channel == "cli" else snmp_device_pendding_dict
        device_task_dict = cli_device_task_dict if channel == "cli" else snmp_device_task_dict


        if device_id in device_task_dict:
            del device_task_dict[device_id]

        # create new task
        if device_id in device_pending_dict:
            
            if channel not in device_q:
                device_q[channel] = Queue.Queue()
            _device_q = device_q[channel]

            task_id = uuid.uuid4().hex
            device_task_dict[device_id] = task_id

            session_mgr.init_parser_queue(task_id)
            device_info = device_pending_dict[device_id]
            session_mgr.put(task_id,
                                dict(status='coll_queue',
                                    device_info=device_info,
                                    timer=timer,
                                    coll_queue_timestamp=timestamp,
                                    channel=channel,
                                    parser_status="queue"
                                    ))
            _device_q.put(device_id)
            del device_pending_dict[device_id]

            zmq_publish.send_string(b'%s task' % channel)
            logging.info('Publish new task %s to %s' % (task_id, channel))
           
    elif result_type == "parser":
        session_mgr.update_parser_result(task_id,result)



class SessionApiHandler(web.RequestHandler):
    def check_origin(self, origin):
        return True

    def get(self, *args):

        method = args[0]
        self.set_header("Content-Type", "application/json")
        if method == 'summary':
            
            summary = {}
            timer = session_mgr.get_timer()
            now = time.time()
            session_data = session_mgr.get_all()
            
            for task_id in session_data:
                task = session_data[task_id]
                s = dict(
                    channel=task['channel'],
                    status=task['status'],
                    create=task['coll_queue_timestamp'],
                    age=int(now - task['timer']),
                    device_id=task["device_info"]["device_id"],
                    device_ip=task["device_info"]["ip"],
                    device_hostname=task["device_info"]["hostname"]
                )
                summary[task_id] = s
            
            self.write(json.dumps(session_data))
        elif method == 'debug':
            data = session_mgr.get_all()
            if not data:
                self.set_status(404)
                data = dict(status='Error', message='No session data')
            self.write(json.dumps(data))
        else:
            self.write(json.dumps(dict(status='error',
                                       message='Not valid request')))
        self.finish()

    def put(self, *args):
        method = args[0]
        self.set_header("Content-Type", "application/json")
        if method == 'timer':
            try:
                params = json.loads(self.request.body)
                polling_interval = params.get('polling_interval', 60)
                absolute_timeout = params.get('absolute_timeout', 3600)
                after_read_timeout = params.get('after_read_timeout', 300)
                session_mgr.set_timer(polling_interval,
                                      absolute_timeout,
                                      after_read_timeout)
                self.write(json.dumps(dict(status='success')))
            except ValueError:
                self.write(json.dumps(dict(status='fail',
                                           message='Not valid timer')))
        else:
            self.write(json.dumps(dict(status='error',
                                       message='Not valid request')))
        self.finish()


if __name__ == '__main__':
    options.define("p", default=7777, help="run on the given port", type=int)
    options.parse_command_line()
    config = Configurations()
    port = options.options.p

    loop = ZMQIOLoop()
    loop.install()
    context = zmq.Context()
    zmq_publish = context.socket(zmq.PUB)
    zmq_publish.bind("tcp://127.0.0.1:%s" % str(config.get_configuration("zmqPublish")))
    zmq_dispatch = context.socket(zmq.REP)
    zmq_dispatch.bind("tcp://127.0.0.1:%s" % str(config.get_configuration("zmqDispatch")))
    zmq_result = context.socket(zmq.PULL)
    zmq_result.bind("tcp://127.0.0.1:%s" % str(config.get_configuration("zmqResult")))
    receiver = ZMQStream(zmq_result)
    receiver.on_recv(on_worker_data_in)


    cli_device_pending_dict = {}
    snmp_device_pendding_dict = {}

    device_q = {}
    #device_task_dict = {"cli":{},"snmp":{}}
    cli_device_task_dict = {}
    snmp_device_task_dict = {}


    #task_dict = {}
    #task_q = {}
    task_dispatcher = TaskDispatcher()
    task_dispatcher.daemon = True
    task_dispatcher.start()

    session_mgr = SessionManager(zmq_publish)
    session_mgr.daemon = True
    session_mgr.start()

    
    print 'Tornado server started on port %d' % port
    print 'Press "Ctrl+C" to exit.\n'
    web.Application([
                    (r'/api/v1/session/?(.*)', SessionApiHandler),
                    (r'/api/v1/(.*)/(.*)', CommandApiHandler)
                    
                     ],
                    autoreload=True).listen(port)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
 

