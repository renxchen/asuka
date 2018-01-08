from dispatch import Dispatch
from Pantheon.Venus.constants import TREE_PATH_SPLIT
from tool import Tool
import json


class Parser(object):
    def __init__(self, param):
        self.parser_params = dict()
        self.get_param_from_request(param)
        pass

    def get_param_from_request(self, param):
        self.parser_params['rules'] = param['rules'] if "rules" in param else {}
        self.parser_params['items'] = param['items'] if "items" in param else []

    def handle(self):
        pass

    def send_request(self):
        pass


class SNMPParser(Parser):
    def __init__(self, param):
        super(CliParser, self).__init__(param)

    def handle(self):
        pass


class CliParser(Parser):
    def __init__(self, param):
        super(CliParser, self).__init__(param)

    def handle(self):
        tool = Tool()
        rules = {}

        for rule in self.parser_params['rules'].values():
            tmp = tool.get_rule_value(rule)
            rules[str(rule['ruleid'])] = tmp
        for item in self.parser_params['items'][0:1]:
            rule_path = CliParser.__split_path(item['tree_path'], item['rule_id'])
            rule_path.reverse()
            raw_data = item['output']
            p = Dispatch(rule_path, rules, raw_data)
            p.dispatch()
            arry = p.get_result()
            print arry

    @staticmethod
    def __split_path(path, rule_id):
        rules = []
        if len(path) == 1:
            rules.append(rule_id)
        else:
            rules = path.split(TREE_PATH_SPLIT)[1:]
            rules.append(rule_id)
        return [str(rule) for rule in rules]


if __name__ == "__main__":
    with open("test_cli_param.json") as f:
        test_cli_param = json.loads(f.read())
    cli_handle = CliParser(test_cli_param)
    cli_handle.handle()