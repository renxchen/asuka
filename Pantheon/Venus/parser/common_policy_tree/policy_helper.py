from Pantheon.Venus.parser.common_policy_tree.db_help import get_all_rule
from Pantheon.Venus.constants import TREE_PATH_SPLIT
from dispatch import Dispatch


def parser(rule_path, all_rules, data):
    if len(rule_path) == 0:
        return
    tmp_rules = {}
    for rule in all_rules:
        tmp_rules[str(rule['ruleid'])] = rule
    the_first_data = tmp_rules[rule_path[0][0]]
    the_first_data['data'] = data
    the_first_data['start_line'] = 0
    the_first_data['end_line'] = len(data.split('\n')) - 1
    p = Dispatch(rule_path, tmp_rules, the_first_data)
    p.dispatch()
    arry = p.get_result()
    print arry


def __get_rule_path(rule_path, all_rules):
    tmp_rules = {}
    return_rule_path = []
    for rule in all_rules:
        tmp_rules[str(rule['ruleid'])] = rule

    for path in rule_path.split(TREE_PATH_SPLIT)[1:]:
        # if path in tmp_rules.keys():
        #     return_rule_path.append(tmp_rules[path])
        # else:
        #     return_rule_path.append(None)
        if path in tmp_rules.keys():
            return_rule_path.append((path, path))
        else:
            return_rule_path.append(None)
    return return_rule_path


if __name__ == "__main__":
    test_rule_path = "/1/3/1/3"
    test_data = None
    with open("test", "r") as f:
        test_data = f.read()
    rules = get_all_rule()
    rule_path = __get_rule_path(test_rule_path, rules)
    parser(rule_path, rules, test_data)



