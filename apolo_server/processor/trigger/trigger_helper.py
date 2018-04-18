from apolo_server.processor.constants import TriggerConstants,CommonConstants

from apolo_server.processor.db_units.db_helper import TriggerDbHelp
from apolo_server.processor.trigger.function_helper import Max, Min, Avg, Hex2Dec, Last, LastRange, handle_expression, \
    _create_item,is_failure_expression
from apolo_server.processor.units import FunctionException
import logging
import time
from multiprocessing.dummy import Pool as ThreadPool
from apolo_server.processor.db_units.memcached_helper import TriggerMemCache,EventMemCache
import traceback

class TriggerHelp(object):
    
    def __init__(self, task, items,clock,logger):
        self.logger = logger
        self.items = items
        self.unhandle_triggers = []

        if clock:
            self.clock = self.get_int_clock(clock)
    
        self.all_parsed_items = []
        if "parser_result" in task:

            for _result in task["parser_result"].itervalues():
                #if _result["status"] == "success":
                self.all_parsed_items.extend(_result["items"])

        self.all_parsed_items.extend(items)

        self.device_id = task["device_info"]["device_id"]

        self.trigger_details = []
        with TriggerMemCache() as cache:
            self.trigger_details = cache.get(self.device_id)
           
            
        self.events=[]
        with EventMemCache() as cache:
            self.events = cache.get(self.device_id)
            

        self.db_events=[]

    def get_int_clock(self,clock):
        clock = float(clock)
        return int(clock)
        
    def get_triggers_by_item(self,item):

        _item_id = item["item_id"]
        triggers = []
        items = []
        item_ids = []
        for trigger in self.trigger_details:
     
            # findA
            if trigger["itemA"] == _item_id :
                # whether has cloumnB
                if trigger["itemB"] is not None:
                    has_find_itemB = False
                    for _parsed_item in self.all_parsed_items:
                        if _parsed_item["item_id"] == trigger["itemB"]:
                            if _item_id not in item_ids:
                                item_ids.append(_item_id)
                                items.append(item)
                            if _parsed_item["item_id"] not in item_ids:
                                item_ids.append(_parsed_item["item_id"])
                                items.append(_parsed_item)

                            triggers.append(trigger)
                            has_find_itemB = True
                            break
                    
                    if not has_find_itemB:
                        #item["expression"] = trigger["expression"]
                        self.unhandle_triggers.append(trigger)
                else:
                    if _item_id not in item_ids:
                        item_ids.append(_item_id)
                        items.append(item)
                    triggers.append(trigger)
        
        return triggers,items

    def is_trigger_valid(self,trigger_id):
        
        for _trigger_detail in self.trigger_details:
            if trigger_id == _trigger_detail["trigger_id"]:
                return True

        return False

    def trigger_expression(self,triggers,items):
        
        if not items:
            return 
        
        triggerd_identifiers = []
        status = items[0]["status"]
        policy_type = items[0]["policy_type"]
        #trigger_type = TriggerConstants.PRIORITY_URGENT_LEVEL_VALUE
        has_failure = False
        if policy_type == CommonConstants.CLI_TYPE_CODE:
            if status ==  "coll_fail":
                has_failure = True
        else:
            if status != "success":
                has_failure = True

        MAX, MIN, AVG, HEX2DEC, LAST, LASTRANGE = Max(), Min(), Avg(), Hex2Dec(), Last(), LastRange()
        for _trigger in triggers:
            _trigger_num = 1
            _triggerd = TriggerConstants.NOT_TRIGERD
            _trigger_status = TriggerConstants.NORMAL_VALUE
            _action = TriggerConstants.NO_ACTION
           
            try:
                
                if has_failure:

                    if _trigger["trigger__trigger_type"]==TriggerConstants.TRIGGER_TYPE_FAILED :
                        exp_triggerd = False
                        if _trigger["trigger_priority"] == TriggerConstants.PRIORITY_URGENT_LEVEL_VALUE:
                            self.db_events.append(dict(
                                clock = self.clock,
                                number = 0,
                                trigger_value = TriggerConstants.TRIGGER_VALUE,
                                trigger_id = _trigger["trigger_id"],
                                triggerd = TriggerConstants.TRIGERD,
                                action=TriggerConstants.TAKE_ACTION
                            ))
                            break
                            
                else:
                    if is_failure_expression(_trigger["expression"],items):
                        continue

                    expression_str = handle_expression(_trigger["expression"],_trigger["trigger__trigger_type"])
                    print expression_str
                    exp_triggerd = eval(expression_str)
                    print exp_triggerd
                
                    if exp_triggerd:
                        _trigger_status = TriggerConstants.TRIGGER_VALUE

                        #has_his_event = False
                        if _trigger["trigger__trigger_limit_nums"] > 1:
                            for event in self.events:
                                if _trigger["trigger_id"] == event["trigger_id"]:
                                    #has_his_event = True
                                    #if event["triggerd"]:
                                    if event["trigger_value"] == TriggerConstants.TRIGGER_VALUE:
                                        _trigger_num = event["number"] + 1
                                    break
                        
                        if _trigger_num >= _trigger["trigger__trigger_limit_nums"]:
                            _trigger_num = 0
                            _triggerd = TriggerConstants.TRIGGERD
                            if _trigger["trigger__identifier"] not in triggerd_identifiers:
                                _action = TriggerConstants.TAKE_ACTION 
                                triggerd_identifiers.append(_trigger["trigger__identifier"])

                    self.db_events.append(dict(
                        clock = self.clock,
                        number = _trigger_num,
                        trigger_value = _trigger_status,
                        trigger_id = _trigger["trigger_id"],
                        triggerd = _triggerd,
                        action = _action
                    ))
                
            except FunctionException, e:
                print traceback.format_exc()
                self.logger.error(str(e))
            except Exception, e:
                print traceback.format_exc()
                self.logger.error(str(e))

    def handle_complex_triggers(self,parser_result):

        #complex_trigger_len
        COMPLEX_EXP_ITEM_LEN = 2
        self.db_events = []
        item_dict = {}

        for _result in parser_result.itervalues():
            if _result["status"] != "success":
                continue
       
            for _trigger in _result["unhandle_triggers"]:
                if self.is_trigger_valid(_trigger["trigger_id"]):
                    #if _trigger["itemA"] in items:
                    
                    triggers = []
                    items=[]
                    for _item in self.all_parsed_items:
                        if len(items) == COMPLEX_EXP_ITEM_LEN:
                            break

                        if _trigger["itemA"] == _item["item_id"] or _trigger["itemB"] == _item["item_id"]:
                            items.append(_item)
    
                    
                    if len(items) == COMPLEX_EXP_ITEM_LEN:
                        data = item_dict.setdefault(_trigger["itemA"],{"triggers":[],"items":[],"item_ids":[],"clock":self.get_int_clock(_result["collection_clock"])})
                        data["triggers"].append(_trigger)
                        for item in items:
                            if item["item_id"] not in data["item_ids"]:
                                data["items"].append(item)
                                data["item_ids"].append(item["item_id"])
        
        for v in item_dict.itervalues():
            self.clock = v["clock"]
            if v["triggers"]:
                self.trigger_expression(v["triggers"],v["items"])
          
        TriggerDbHelp.save_events(self.db_events,int(self.device_id))

    def cache_event(self):

        with EventMemCache() as cache:
            self.events = cache.set(self.device_id)
        
    def trigger(self):

        self.db_events = []
        for item in self.items:
            triggers,trigger_items = self.get_triggers_by_item(item)
            if triggers:
                self.trigger_expression(triggers,trigger_items)
        
        TriggerDbHelp.save_events(self.db_events,int(self.device_id))

if __name__ == "__main__":
    pass
    # pool = ThreadPool(20)
    # t1 = time.clock()
    # for i in range(0, 1):
    #     pool.apply_async(__test)
    # pool.close()
    # pool.join()
    # print time.clock() - t1
    #__test()