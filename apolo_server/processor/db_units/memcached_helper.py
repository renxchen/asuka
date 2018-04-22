import memcache
import logging
import time
from apolo_server.processor.constants import CommonConstants
from db_helper import DeviceDbHelp,TriggerDbHelp


class MemCacheBase(object):

    def __init__(self, timeout=2):
        self.AUTO_SAVE_CACHE = True
        self.key = None
        self.timeout = timeout
        self._mc = ""

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return False
        self._disconnect_all()
        return True

    def _connect(self):
        self._mc = memcache.Client(CommonConstants.MEM_CACHE_HOSTS, debug=True)

    def get(self):
        # if self.AUTO_UPDATE_LATEST or auto_update_latest:
        #     self.delete()
        data = self._mc.get(self.key)
        if data is not None:
            logging.debug("Get data from memory cache")
        else:
            data = self.do_get()
            if self.AUTO_SAVE_CACHE:
                self.set(data)
        return data

    def set(self, value):
        self._mc.set(self.key, value)

    def update(self):
        data = self.do_get()
        self.set(data)
        return data

    def do_get(self):
        pass
        return []

    def cache(self):
        data = self._mc.get(self.key)
        if data is None:
            data = self.do_get()
            if self.AUTO_SAVE_CACHE:
                self.set(data)

    def flush_all(self):
        self._mc.flush_all()

    def delete(self):
        self._mc.delete(self.key)

    def _disconnect_all(self):
        self._mc.disconnect_all()


class LastCheckTimeMemCache(MemCacheBase):
    def __init__(self):
        super(LastCheckTimeMemCache, self).__init__()
        self.key = "Last_Check_Time"

    def get(self, schedule_id):
        data = self._mc.get(self.key)
        if data:
            logging.debug("Get data from memory cache")
        else:
            data = self.do_get()
            if self.AUTO_SAVE_CACHE:
                self.set(data)
        return data

class BatchMemCacheBase(MemCacheBase):
    def __init__(self):
        super(BatchMemCacheBase, self).__init__()
        self.key_prefix = ""

    def multi_set(self, data_dict):
        return self._mc.set_multi(data_dict, key_prefix=self.key_prefix)

    def multi_get(self, keys):
        return self._mc.get_multi(keys, key_prefix=self.key_prefix)


class TriggerMemCache(BatchMemCacheBase):
    def __init__(self):

        super(TriggerMemCache, self).__init__()
        self.key_prefix = "trigger_"

    def get(self,device_id):
        
        search_key = self.key_prefix+device_id
        data = self._mc.get(search_key)
        if data is not None:
            logging.debug("Get data from memory cache")
        else:

            data = TriggerDbHelp.get_triggerDetail_by_deviceid(int(device_id))
            self._mc.set(search_key, data)
            #if self.AUTO_SAVE_CACHE:
            #self.set(data)
        return data

class EventMemCache(MemCacheBase):
    def __init__(self):
        super(EventMemCache, self).__init__()
        self.key_prefix = "event_"

    def get(self,device_id):
        search_key = self.key_prefix+device_id
        data = self._mc.get(search_key)
        if data is not None:
            logging.debug("Get data from memory cache")
        else:
            data = TriggerDbHelp.get_latest_event(device_id)
            self._mc.set(search_key, data)
            #if self.AUTO_SAVE_CACHE:
            #self.set(data)
        return data
    
    def set(self,device_id):
        search_key = self.key_prefix+device_id
        data = TriggerDbHelp.get_latest_event(device_id)
        self._mc.set(search_key, data)


if __name__ == "__main__":
    pass
    # with RulesMemCacheDb() as item:
    #     print item.get()
    # with TriggerMemCache() as cache:
    #     data = TriggerDbHelp.get_triggerDetail_by_deviceid(2042)
    #     cache._mc.set("trigger_2042", data)
    #     print cache.get("2042")     
    with EventMemCache() as cache:
        print cache.set("2042")

    with TriggerMemCache() as cache:
        cache._mc.delete("trigger_2042")








