# -*- coding: utf-8 -*-

__author__ = 'Zhu Tong <zhtong@cisco.com>'
__version__ = '0.5'

import Queue
import json
import logging
import time
import uuid
from threading import Thread

import requests
import zmq
from tornado import web, ioloop, options
from zmq.eventloop.ioloop import ZMQIOLoop
from zmq.eventloop.zmqstream import ZMQStream

from credential_mgr import CredentialManager
from session_mgr import SessionManager


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


class CommandApiHandler(web.RequestHandler):
    @web.asynchronous
    def post(self, *args):
        self.set_header("Content-Type", "application/json")
        method = args[0]
        category = args[1]
        params = json.loads(self.request.body)

        if method not in 'callback polling sync':
            self.write(json.dumps(dict(status='error',
                                       message='Not support method')))
            self.finish()
            return

        # callback mode must be given a callback url
        if method == 'callback':
            cb_url = params.get('url')
            if not cb_url:
                self.write(json.dumps(dict(status='error',
                                           message='No callback url')))
                self.finish()
                return

        # get commands
        commands = params.get('commands')
        if not commands:
            self.write(json.dumps(dict(status='error',
                                       message='No valid commands')))
            self.finish()
            return

        # device_id can be hostname or ip address
        ip = params.get('ip')
        hostname = params.get('hostname')
        if not (ip or hostname):
            self.write(json.dumps(dict(status='error',
                                       message='No valid ip or hostname')))
            self.finish()
            return

        # get credential from local based on ip or hostname
        device_info_res = None
        if ip:
            device_info_res = credential.get(ip)
            if device_info_res['status'] == 'error':
                if hostname:
                    device_info_res = credential.get(hostname)
        if device_info_res and device_info_res['status'] == 'ok':
            device_info = device_info_res['device_info']
            device_info.update(params)
        else:
            device_info = params

        if category == 'cli':
            if 'username' not in device_info or 'password' not in device_info:
                common = credential.common
                device_info['username'] = common['username']
                device_info['password'] = common['password']
                # self.write(json.dumps(dict(status='error',
                #                            message='No username or password!')))
                # self.finish()
                # return
        elif category == 'snmp':
            if 'community' not in device_info:
                self.write(json.dumps(dict(status='error',
                                           message='No community!')))
                self.finish()
                return

        # create new task
        task_id = uuid.uuid4().hex
        timer = time.time()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        session_mgr.put(task_id,
                        dict(status='Queue',
                             method=method,
                             commands=commands,
                             device_info=device_info,
                             timer=timer,
                             timestamp=timestamp,
                             read=False,
                             category=category))

        # determine worker's channel
        if category == 'cli':
            channel = device_info.get('platform', 'ios')
        else:
            channel = category

        # put task into queue by the channel
        if channel not in task_q:
            task_q[channel] = Queue.Queue()
        q = task_q[channel]
        q.put(task_id)

        if method == 'polling':
            self.write(json.dumps(dict(url='/api/v1/task/%s' % task_id)))
            self.finish()

        elif method == 'sync':
            def cb_func(response, *args):
                self.write(json.dumps(response, indent=2))
                self.finish()
                session_mgr.set_read(task_id)
                del task_dict[task_id]

            task_dict[task_id] = cb_func, None

        elif method == 'callback':
            def cb_func(response, url):
                task_id = response.get('task_id')
                body = json.dumps(response, indent=2)
                logging.info('Callback for task %s to %s' % (task_id, url))
                cb_res = requests.post(url, data=body)
                logging.info('Callback for task %s done, status: %s' % (task_id, cb_res.status_code))
                session_mgr.set_read(task_id)
                del task_dict[task_id]

            task_dict[task_id] = cb_func, cb_url

            self.write({'status': 'ok',
                        'message': 'Will callback to %s' % cb_url})
            self.finish()

        # publish the new task to the channel
        zmq_publish.send_string(b'%s task' % channel)
        logging.info('Publish new task %s to %s' % (task_id, channel))


class TaskApiHandler(web.RequestHandler):
    def check_origin(self, origin):
        return True

    def get(self, *args):
        task_id = args[0]
        self.set_header("Content-Type", "application/json")

        data = session_mgr.get(task_id)
        if not data:
            self.set_status(404)
            self.write(json.dumps(dict(status='Error',
                                       message='Not found')))
        else:
            if data['status'] == 'finish':
                self.write(json.dumps(data['result']))
            else:
                self.write(json.dumps(dict(status=data['status'])))
        self.finish()


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
                    category=task['category'],
                    status=task['status'],
                    has_read=task['read'],
                    create=task['timestamp'],
                    age=int(now - task['timer']),
                    method=task['method']
                )
                summary[task_id] = s
            self.write(json.dumps(dict(timer=timer,
                                       summary=summary)))
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


class CredentialApiHandler(web.RequestHandler):
    def check_origin(self, origin):
        return True

    def post(self, *args):  # Create
        device_id = args[0]
        self.set_header("Content-Type", "application/json")
        if not device_id:  # Create multiple devices
            try:
                params = json.loads(self.request.body)
                res = credential.create_m(params)
                self.write(json.dumps(res))
            except ValueError:
                self.write(json.dumps(dict(status='fail',
                                           message='Not valid fields')))
        else:
            try:
                params = json.loads(self.request.body)
                res = credential.create(**params)
                self.write(json.dumps(res))
            except ValueError:
                self.write(json.dumps(dict(status='fail',
                                           message='Not valid fields')))
        credential.save()
        self.finish()

    def get(self, *args):  # Read
        device_id = args[0]
        self.set_header("Content-Type", "application/json")
        self.set_header('Access-Control-Allow-Origin', '*')
        if not device_id:
            result = credential.get_all()
        else:
            result = credential.get(device_id)
        self.write(json.dumps(result))
        self.finish()

    def put(self, *args):  # Update
        device_id = args[0]
        self.set_header("Content-Type", "application/json")
        if not device_id:  # Update multi devices
            params = json.loads(self.request.body)
            result = credential.update_m(params)
            self.write(json.dumps(result))
        else:  # Update one device
            try:
                params = json.loads(self.request.body)
                result = credential.update(device_id, **params)
                self.write(json.dumps(result))
            except ValueError:
                self.write(json.dumps(dict(status='fail',
                                           message='Not valid fields')))
        credential.save()
        self.finish()

    def delete(self, *args):  # Delete
        device_id = args[0]
        self.set_header("Content-Type", "application/json")
        if not device_id:
            self.write(json.dumps(dict(status='fail',
                                       message='Device not given')))
        else:
            self.write(json.dumps(credential.delete(device_id)))
            credential.save()
        self.finish()


class CredentialCommonApiHandler(web.RequestHandler):
    def check_origin(self, origin):
        return True

    def get(self, *args):
        self.set_header("Content-Type", "application/json")
        self.set_header('Access-Control-Allow-Origin', '*')

        self.write(json.dumps(credential.common))
        self.finish()

    def put(self, *args):  # Update
        self.set_header("Content-Type", "application/json")
        params = json.loads(self.request.body)
        result = credential.set_common(params)
        self.write(json.dumps(result))
        credential.save()
        self.finish()


class DeviceApiHandler(web.RequestHandler):
    def check_origin(self, origin):
        return True

    def get(self, *args):
        q = args[0].lower()
        self.set_header("Content-Type", "application/json")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write(json.dumps(credential.query(q)))
        self.finish()


# Worker push result to command center
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
    except TypeError:
        pass


if __name__ == '__main__':
    options.define("p", default=8080, help="run on the given port", type=int)
    options.parse_command_line()
    port = options.options.p

    # logging = get_logging('CmdCenter', logging.INFO)

    loop = ZMQIOLoop()
    loop.install()
    context = zmq.Context()
    # zmq socket 用来通知workers有新任务
    zmq_publish = context.socket(zmq.PUB)
    zmq_publish.bind("tcp://*:6000")
    # zmq socket 用来发送任务给Worker
    zmq_dispatch = context.socket(zmq.REP)
    zmq_dispatch.bind("tcp://*:6001")
    # zmq socket 用来接收Worker的任务结果
    zmq_result = context.socket(zmq.PULL)
    zmq_result.bind("tcp://*:6002")
    
    receiver = ZMQStream(zmq_result)
    receiver.on_recv(on_worker_data_in)

    session_mgr = SessionManager()
    session_mgr.daemon = True
    session_mgr.start()

    task_dict = {}
    task_q = {}
    task_dispatcher = TaskDispatcher()
    task_dispatcher.daemon = True
    task_dispatcher.start()

    credential = CredentialManager()

    print('Tornado server started on port %d' % port)
    print('Press "Ctrl+C" to exit.\n')

    web.Application([(r'/api/v1/task/?(.*)', TaskApiHandler),
                     (r'/api/v1/session/?(.*)', SessionApiHandler),
                     (r'/api/v1/credential_common/?', CredentialCommonApiHandler),
                     (r'/api/v1/credential/?(.*)', CredentialApiHandler),
                     (r'/api/v1/device/?(.*)', DeviceApiHandler),
                     (r'/api/v1/(.*)/(.*)', CommandApiHandler),
                     ],
                    autoreload=True,
                    ).listen(port)

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
