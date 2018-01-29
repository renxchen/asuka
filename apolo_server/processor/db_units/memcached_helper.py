import memcache
import logging
from apolo_server.processor.constants import CommonConstants
from db_helper import DeviceDbHelp


class MemCacheBase(object):
    def __init__(self):
        self._mc = memcache.Client(CommonConstants.MEM_CACHE_HOSTS, debug=True)
        self.AUTO_SAVE_CACHE = True
        self.key = None
        pass

    def get(self):
        data = self._mc.get(self.key)
        if data:
            logging.debug("Get data from memory cache")
        else:
            data = self.do_get()
            if self.AUTO_SAVE_CACHE:
                self.set(data)
        return data

    def set(self, value):
        self._mc.set(self.key, value)

    def _update(self):
        data = self.do_get()
        self._set(data)

    def do_get(self):
        pass
        return []

    def flush_all(self):
        self._mc.flush_all()


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
        rules = DeviceDbHelp.get_all_rule()
        result = [rule for rule in rules]
        return result

if __name__ == "__main__":
    item = RulesMemCacheDb()
    # item.flush_all()
    for i in item._get():
        print i






