import re
from backend.apolo.tools import constants
import simplejson as json


class DataExtractPolicy(object):
    def __init__(self, data, **extract_policy):
        self.data = data
        self.extract_policy = extract_policy

    def x_offset_extract(self):
        count = 0
        start = self.extract_policy['start_line']
        end = self.extract_policy['end_line']
        offset = self.extract_policy['x_offset']
        basic_c = self.extract_policy['basic_characters']
        split_c = self.extract_policy['split_characters']
        render_b_c = ''
        if split_c is constants.SPLIT_RULE_SPACE:
            render_b_c = constants.SPACE_INSTEAD.join(basic_c.split())
        extract_regexp = self.extract_policy['extract_regexp']
        raw_data_list = self.data.split('\n')[start:end + 1]
        count_mark = False
        result = []
        for i in range(len(raw_data_list)):
            if basic_c in raw_data_list[i]:
                raw_data_list[i] = raw_data_list[i].replace(basic_c, render_b_c)
        new_list = ''.join(raw_data_list).split()
        if offset < 0:
            # new_list = new_list[:new_list.index(render_b_c) + 1]
            new_list.reverse()
            # offset *= -1
        for i in range(len(new_list)):
            pattern = re.compile(render_b_c)
            m = re.search(pattern, new_list[i])
            if m is not None:
                count_mark = True
                result.append(i)
                continue
            if '' is new_list[i]:
                continue
            if count_mark and new_list[i] is not '':
                count += 1
            if count == int(str(offset).replace('-', '')):
                pattern = re.compile(extract_regexp)
                m = re.search(pattern, new_list[i])
                if m is not None:
                    result.append(i)
                break
        # print result, new_list[result[0]], new_list[result[-1]]
        if offset < 0:
            result = [len(new_list) - 1 - result[-1], len(new_list) - 1 - result[0]]
        res = {
            'start_line': start,
            'end_line': end,
            'data_extract_mark': {
                'basic_character_index': result[0],
                'extract_data_index': result[-1]
            }
        }
        print res
        return res

    def y_offset_extract(self):
        pass


def test():
    data = '''GigabitEthernet0/0/0 is up, line protocol is up
                  Hardware is 4XGE-BUILT-IN, address is 2c54.2d61.7200 (bia 2c54.2d61.7200)
                  Internet address is 10.92.51.106/30
                  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
                     Available Flows        = 70495509
                     Received 0 broadcasts (0 IP multicasts)
    '''
    extract_policy = {
        'basic_characters': 'Available Flows',
        'split_characters': 'space',
        'x_offset': 2,
        'y_offset': 2,
        'extract_regexp': '\d+',
        'start_line': 0,
        'end_line': 5,
    }
    d = DataExtractPolicy(data, **extract_policy)
    d.x_offset_extract()


test()
