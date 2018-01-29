__author__ = 'zhutong'

"""
A very simple session/cache manager for testing
Should be implemented using redis
"""

from threading import Thread
import time
from helper import get_logger


class SessionManager(Thread):
    data_set = {}
    polling_interval = 60
    absolute_timeout = 3600
    after_read_timeout = 300

    def put(self, k, v):
        self.data_set[k] = v

    def update(self, k, v):
        try:
            self.data_set[k].update(v)
        except KeyError:
            pass

    def get(self, k):
        data = self.data_set.get(k)
        if data:
            data['timer'] = time.time()
            data['read'] = True
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
            if after_read_timeout >= 60:
                self.after_read_timeout = after_read_timeout
            if polling_interval >= 5:
                self.polling_interval = polling_interval
        except ValueError:
            pass

    def run(self):
        logger = get_logger('SessionMgr')
        while True:
            time.sleep(self.polling_interval)
            for k in self.data_set.keys():
                v = self.data_set[k]
                if time.time() - v['timer'] > self.absolute_timeout:
                    del self.data_set[k]
                    logger.info('Task %s timeout, cleared' % k)
                elif v['read'] and time.time() - v['timer'] > self.after_read_timeout:
                    del self.data_set[k]
                    logger.info('Task %s timeout, cleared' % k)
