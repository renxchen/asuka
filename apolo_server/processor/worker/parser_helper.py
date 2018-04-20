
from backend.apolo.apolomgr.resource.common.common_policy_tree.dispatch import Dispatch
from apolo_server.processor.constants import ParserConstants, CommonConstants
from apolo_server.processor.db_units.db_helper import ParserDbHelp
import traceback

class ParserHelp(object):

    def __init__(self,clock,logger):
        self.logger = logger
        self.items = []
        self.result = {}

        clock = clock.split(".")
        self._clock = int(clock[0])
        self._ns = int(clock[1])
        self.device_log_info = ""


    def parse(self,task,clock):
        
        result = task["element_result"][clock]
        item_type = CommonConstants.CLI_TYPE_CODE if task["channel"].upper() == "CLI" \
                            else CommonConstants.SNMP_TYPE_CODE
        
        deviceinfo = task["device_info"]
        self.device_log_info = "Device ID: %s,IP: %s,HostName: %s" % (deviceinfo["device_id"],deviceinfo["ip"],deviceinfo["hostname"])

        time_prefix = ["1day","1hour","15min","5min","1min"]
        oid_dict = {}
        status = result.get("status","")
        message = result.get("message","")
    
        if status!= "success":
            raise Exception(message)

        if item_type == CommonConstants.SNMP_TYPE_CODE:
            for data in result["output"]:
                oid_dict[data["origin_oid"]] = {"status":data["status"],"value":data["value"],"message":data["message"]}
    
        for _prefix in time_prefix:
            _itemkey = "items_%s" % _prefix
            if _itemkey  not in deviceinfo:
                continue
            
            for item in deviceinfo[_itemkey]:
                if item_type == CommonConstants.SNMP_TYPE_CODE:
                    tmp_oid_dict = oid_dict[item["oid"]]
                    #status = tmp_oid_dict.get("status","")
                    if item["oid"] in oid_dict:
                        item.update(oid_dict[item["oid"]])
                        self.items.append(item)
                         
                else:
                    if item["command"] == result["command"]:
                        item["message"] = result["message"]
                        item["status"] = result["status"]
                        self.items.append(item)
    
        if item_type == CommonConstants.SNMP_TYPE_CODE:
            self.snmp_parse()
        else:
            self.cli_parse(result["output"])

    def snmp_parse(self):
        
        for item in self.items:
            if item["status"] == "success":
                try:
                    value_type = item['value_type']
                    ParserDbHelp.snmp_save(value_type, [item["item_id"],self._clock,self._ns,item["value"]])
                except Exception as e:
                    self.logger.error(self.device_log_info + " "+ str(e))
                    print traceback.format_exc()
                    item["status"] = "fail"
                    item["message"] = str(e)

    def cli_parse(self,data):

        for item in self.items:
            if item["status"] != "success":
                continue
            print str(item["item_id"])+":"+str(item["rule_path"])
            p = Dispatch(item["rule_path"], item["rules"], data)
            p.dispatch()
            arry = p.get_result()
            item_id = item['item_id']
            item['values'] = []
            item['block_paths'] = []
            item['errors']=[]

            for parent_item in arry:
                for seq,child_item in enumerate(parent_item):
                    if child_item.has_key('extract_match_flag'):
                        if child_item['extract_match_flag']:
                            value = child_item['extract_data']
                            if value:
                                value = value[0]
                            else:
                                value = None

                            value_type = item['value_type']
                            cli_data = [item["item_id"],self._clock,self._ns,seq,value,child_item["block_path"]]
                              
                            try:
                                ParserDbHelp.cli_save(value_type,cli_data)
                                item['values'].append(value)
                                item['block_paths'].append(child_item["block_path"])
                                #item["block_path"] = child_item["block_path"]
                            except Exception as e:
                                self.logger.error(self.device_log_info + " "+ str(e))
                                item['errors'].append({"seq":seq,"db_message":str(e)})
                                #item["status"] = "fail"
                                #item["message"] = str(e)

                        else:
                            item['errors'].append({"seq":seq,"parser_message": child_item["error_msg"]})
                            self.logger.error("%s CLI PARSE ERROR, ITEM_ID:%d Error_Info:%s " % (self.device_log_info, item_id, child_item["error_msg"]))
            
            if len(item['values']) == 0:
                item["status"] = "fail"

            del item["rules"]
            del item["rule_path"]
    
    def get_items(self):
        return self.items
            
if __name__ == "__main__":
    import json
    data={}
    with open("/Users/yihli/Desktop/projects/apolo/apolo_server/processor/worker/a","rb") as f123:
        content = f123.read()
        print content
        f_data = json.loads(content)

    for item in f_data["items"]:
        if item["status"] != "success":
            continue
    
        p = Dispatch(item["rule_path"], item["rules"], f_data["data"])
        p.dispatch()
        arry = p.get_result()
        item_id = item['item_id']
        item['values'] = []
        item['block_paths'] = []
        item['errors']=[]

        for parent_item in arry:
            for seq,child_item in enumerate(parent_item):
                if child_item.has_key('extract_match_flag'):
                    if child_item['extract_match_flag']:
                        value = child_item['extract_data']
                        if value:
                            value = value[0]
                        else:
                            value = None

                        value_type = item['value_type']
                        print child_item
                        cli_data = [item["item_id"],0,0,seq,value,child_item["block_path"]]
                            
                        try:
                            ParserDbHelp.cli_save(value_type,cli_data)
                            item['values'].append(value)
                            item['block_paths'].append(child_item["block_path"])
                            #item["block_path"] = child_item["block_path"]
                        except Exception as e:
                            #self.logger.error(self.device_log_info + " "+ str(e))
                            item['errors'].append({"seq":seq,"db_message":str(e)})
                            #item["status"] = "fail"
                            #item["message"] = str(e)

                    else:
                        item['errors'].append({"seq":seq,"parser_message": child_item["error_msg"]})
                        #self.logger.error("%s CLI PARSE ERROR, ITEM_ID:%d Error_Info:%s " % (self.device_log_info, item_id, child_item["error_msg"]))
        
        if len(item['values']) == 0:
            item["status"] = "fail"

        del item["rules"]
        del item["rule_path"]