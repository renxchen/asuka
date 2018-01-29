from dispatch import Dispatch
from Pantheon.Venus.constants import ParserConstants, CommonConstants
from tool import Tool
from db_help import bulk_save_result
import json


class Parser(object):
    def __init__(self, param):
        self.parser_params = dict()
        self.get_param_from_request(param)
        pass

    def get_param_from_request(self, param):
        self.parser_params['rules'] = param['parser_params']['rules']
        self.parser_params['items'] = param['items'] if "items" in param else []
        # self.parser_params['task_timestamp'] = param['task_timestamp'] if "task_timestamp" in param else 0
        for item in self.parser_params['items']:
            item['task_timestamp'] = param['task_timestamp'] if "task_timestamp" in param else 0

    def handle(self):
        pass

    def send_request(self):
        pass


class SNMPParser(Parser):
    def __init__(self, param):
        super(SNMPParser, self).__init__(param)

    def handle(self):
        bulk_save_result(self.parser_params['items'], CommonConstants.SNMP_TYPE_CODE)
        pass


class CliParser(Parser):
    def __init__(self, param):
        super(CliParser, self).__init__(param)

    def handle(self):
        tool = Tool()
        rules = {}
        result = []

        for rule in self.parser_params['rules'].values():
            tmp = tool.get_rule_value(rule)
            rules[str(rule['ruleid'])] = tmp

        for item in self.parser_params['items']:

            rule_path = CliParser.__split_path(item['tree_path'], item['rule_id'])
            raw_data = item['output']

            p = Dispatch(rule_path, rules, raw_data)

            p.dispatch()
            arry = p.get_result()
            if len(arry) == 0:
                continue
            item['value'] = arry[-1][0]
            result.append(item)
        bulk_save_result(result, CommonConstants.CLI_TYPE_CODE)

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
    if item_type == CommonConstants.CLI_TYPE_CODE:
        func = CliParser(params)
    else:
        func = SNMPParser(params)
    func.handle()


if __name__ == "__main__":
    with open("test_cli_param.json") as f:
        test_cli_param = json.loads(f.read())
    cli_handle = CliParser(test_cli_param)
    cli_handle.handle()
    # with open("test_snmp_param.json") as f:
    #     test_snmp_param = json.loads(f.read())
    # snmp_handle = SNMPParser(test_snmp_param)
    # snmp_handle.handle()