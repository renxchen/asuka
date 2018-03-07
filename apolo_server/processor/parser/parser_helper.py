import sys
from apolo_server.processor.parser.common_policy_tree.dispatch import Dispatch
from apolo_server.processor.constants import ParserConstants, CommonConstants
from apolo_server.processor.parser.common_policy_tree.tool import Tool
from apolo_server.processor.db_units.memcached_helper import ItemMemCacheDb, RulesMemCacheDb
from apolo_server.processor.db_units.db_helper import ParserDbHelp
from multiprocessing.dummy import Pool as ThreadPool
import threading
import json
import os
import logging
import time
import thread

class Parser(object):
    def __init__(self, param):
        self.parser_params = dict()
        self.timestamp = 0
        #self.items = []
        self.get_param_from_request(param)

    def get_param_from_request(self, param):
        
        #self.parser_params['rules'] = rules
        self.parser_params['items'] = param['items']
        self.timestamp = param['task_timestamp']
        for item in self.parser_params['items']:
            #self.items.append(item)
            item['task_timestamp'] = param['task_timestamp'] if "task_timestamp" in param else 0

    def handle(self):
        pass

    def send_request(self):
        pass


class SNMPParser(Parser):
    def __init__(self, param):
        super(SNMPParser, self).__init__(param)

    def handle(self):
        ParserDbHelp().bulk_save_result(self.parser_params['items'], CommonConstants.SNMP_TYPE_CODE)
        pass


class CliParser(Parser):

    
    def __init__(self, param):
        super(CliParser, self).__init__(param)
       

    def handle(self):
        
        rules = {}
        with RulesMemCacheDb() as rules:
            rules = rules.get()
        print rules
        result = []

        for item in self.parser_params['items']:
            rule_path = CliParser.__split_path(item['tree_path'],
                                               item['rule_id'])
            raw_data = item['output']
            if raw_data is None:
                continue

            p = Dispatch(rule_path, rules, raw_data)
            p.dispatch()
            arry = p.get_result()
            item['value'] = arry[-1][0]
            result.append(item)
        ParserDbHelp().bulk_save_result(result, CommonConstants.CLI_TYPE_CODE)

    @staticmethod
    def __split_path(path, rule_id):
        rules = []
        if len(path) == 1:
            rules.append(rule_id)
        else:
            rules = path.split(ParserConstants.TREE_PATH_SPLIT)[1:]
            rules.append(rule_id)
        return [str(rule) for rule in rules]


def parser_main(item_type, params):

    def __wrapper(items):
        result = {}
        for item in items:
            if item['item_id'] not in result:
                result[item['item_id']] = {
                    "value_type": CommonConstants.VALUE_TYPE_MAPPING.get(item['value_type']),
                    "policy_type": CommonConstants.ITEM_TYPE_MAPPING.get(item['policy_type']),
                    "item_id": item['item_id']
                }
        return result
    if item_type == CommonConstants.CLI_TYPE_CODE:
        func = CliParser(params)
    else:
        func = SNMPParser(params)
    func.handle()
    items = __wrapper(func.parser_params['items'])
    return items, func.timestamp


if __name__ == "__main__":
    start_time = time.time()
    with open("test_cli_param.json") as f:
        test_cli_param = json.loads(f.read())

    parser_main(0, test_cli_param)
    # items, timestamp = parser_main(item_type=0, params=test_cli_param)
    end_time = time.time()
    print end_time - start_time
    
    
    #pool = ThreadPool(20)
    #for i in range(0, 1000):
    #    pool.apply_async(parser_main, args=(0, test_cli_param))
    #pool.close()
    #pool.join()
    # trigger = TriggerHelp(items, logging)
    # trigger.trigger(task_timestamp=123)
    # cli_handle = CliParser(test_cli_param)
    # cli_handle.handle()
    # with open("test_snmp_param.json") as f:
    #     test_snmp_param = json.loads(f.read())
    # snmp_handle = SNMPParser(test_snmp_param)
    # snmp_handle.handle()