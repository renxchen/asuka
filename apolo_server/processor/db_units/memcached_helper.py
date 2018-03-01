import memcache
import logging
import time
from apolo_server.processor.constants import CommonConstants
from db_helper import DeviceDbHelp
from apolo_server.processor.parser.common_policy_tree.tool import Tool

class MemCacheBase(object):

    def __init__(self, timeout=2):
        self.AUTO_SAVE_CACHE = True
        self.key = None
        self.timeout = timeout
        pass

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect_all()
        return self

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

    def flush_all(self):
        self._mc.flush_all()

    def delete(self):
        self._mc.delete(self.key)

    def _disconnect_all(self):
        self._mc.disconnect_all()


class LastCheckTimeMemCache(MemCacheBase):
    def __init__(self):
        super(ItemMemCacheDb, self).__init__()
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


class ItemMemCacheDb(MemCacheBase):
    def __init__(self):
        super(ItemMemCacheDb, self).__init__()
        self.key = "DB_Item"

    def do_get(self):
        items = DeviceDbHelp.get_all_items_from_db()
        result = [item for item in items]
        return result


class RulesMemCacheDb(MemCacheBase):
    def __init__(self):
        super(RulesMemCacheDb, self).__init__()
        self.key = "DB_Rules"

    def do_get(self):
        rule_dict = {}
        rules = DeviceDbHelp.get_all_rule()
        ruletool = Tool()
        for rule in rules:
            format_rule = ruletool.get_rule_value(rule)
            rule_dict[str(rule['ruleid'])] = format_rule
        return rule_dict


class TaskRunningMemCacheDb(MemCacheBase):
    def __init__(self):
        super(TaskRunningMemCacheDb, self).__init__()
        self.key = "Task_Running_Status"

    def do_get(self):
        return False


if __name__ == "__main__":
    # with RulesMemCacheDb() as item:
    #     print item.get()

    with TaskRunningMemCacheDb() as cache:
        print cache.get()
    # item.flush_all()
    # for i in item._get():
    #     print i






