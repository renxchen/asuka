from backend.apolo.db_utils.db_until import *
from backend.apolo.models import Items
import time


def deco_item(func):
    def wrapper(self, item, now_time):
        if "valid_status" in item.keys():
            if item['valid_status'] is False:
                return item
        status = func(self, item, now_time)
        item['valid_status'] = status
        return item
    return wrapper


class CollectionValidate(object):
    OPEN_VALID_PERIOD_TYPE = 1
    VALID_PERIOD_SPLIT = ";"
    VALID_DATE_FORMAT = "%Y-%m-%d@%H:%M"
    SCHEDULE_GET_NORMALLY = 0
    SCHEDULE_CLOSED = 1
    SCHEDULE_SPECIALLY = 2
    SCHEDULE_WEEKS_SPLIT = ";"
    SCHEDULE_DATE_SPLIT = "@"
    SCHEDULE_SPLIT = "-"
    CLI_COLLECTION_DEFAULT_METHOD = 'telnet'
    SNMP_COLLECTION_DEFAULT_METHOD = "bulk_get"
    """
    Collection Validate
    """
    def __init__(self):
        self.items = []

    @staticmethod
    def get_items(item_type):
        param_dict = {"policys_groups__status": 1, "status": 1, "schedule__status": 1}
        if item_type is not None:
            param_dict["item_type"] = item_type

        items = Items.objects.filter(
            **param_dict).order_by(
            "-policys_groups__exec_interval","schedule__priority").values(
            "item_id",
            "schedule__valid_period_type",
            "schedule__start_period_time",
            "schedule__end_period_time",
            "schedule__data_schedule_type",
            "schedule__data_schedule_time",
            "last_exec_time",
            "item_type",
            "item_id",
            "device__device_id",
            "device__ip",
            "device__hostname",
            "device__login_expect",
            "device__ostype__start_default_commands",
            "device__ostype__snmp_timeout",
            "device__ostype__telnet_timeout",
            "device__login_expect",
            "device__telnet_port",

            "device__snmp_port",
            "device__snmp_community",
            "device__snmp_version",
            "coll_policy__name",
            "coll_policy__cli_command",
            "coll_policy__snmp_oid",

            "coll_policy_rule_tree_treeid",
            "coll_policy_rule_tree_treeid__rule_id_path",
            "coll_policy_rule_tree_treeid__rule_id",
            "coll_policy_rule_tree_treeid__rule__value_type",
            "coll_policy__value_type",
            "schedule__priority",
            "policys_groups__exec_interval",
            "policys_groups__history",
            "policys_groups__policy_group_id",
            "policys_groups__policy_group_id__name",
            "coll_policy_id",
            "value_type",
            "coll_policy_id")
        return list(items)

    def valid_items(self, now_time):
        item_prioriy_dict = {}
        valid_items = []
        self.items = self.get_items(None)
        for index, item in enumerate(self.items):
            item['valid_status'] = True
            self.__check_period_time(item, now_time)
            self.__check_schedule_time(item, now_time)
            self.__check_device_priority(item, item_prioriy_dict, index)

        for item in self.items:
            self.__check_is_stop_collection(item)
            if item['valid_status']:
                valid_items.append(item)




        # for item in self.items:
        #     """
        #         set device's priority status
        #     """
        #     priority_key = "%d_%d" % (item["coll_policy_id"], item["device__device_id"])
        #     if item["valid_status"]:
        #         if priority_key in item_prioriy_dict and not item_prioriy_dict[priority_key]["valid"] \
        #                 and item["item_id"] == item_prioriy_dict[priority_key]["item_id"]:
        #
        #             item["valid_status"] = False
        #
        #         """
        #         filter stop collection
        #         """
        #         self.__check_is_stop_collection(item)
        #
        #     # if item["valid_status"]:
        #     #     valid_items.append(item)
        #
        return self.items

    def __check_is_stop_collection(self, item):
        if item["schedule__data_schedule_type"] == self.SCHEDULE_CLOSED:
            item['valid_status'] = False
        else:
            item['valid_status'] = True
        return


    def __check_device_priority(self, item, item_prioriy_dict, index):
        result = {}
        """
        check priority
        """

        if "valid_status" in item.keys() and item['valid_status']:
            item_key = "%d_%d" % (item["coll_policy_id"], item["device__device_id"])
            if item_key in item_prioriy_dict:
                tmp_p_item = self.items[item_prioriy_dict[item_key]]
                if item["schedule__priority"] > tmp_p_item["schedule__priority"]:
                    item['valid_status'] = True
                    tmp_p_item['valid_status'] = False
                    item_prioriy_dict[item_key] = index
                else:
                    item['valid_status'] = False
            else:
                item_prioriy_dict[item_key] = index
        return

    def __check_schedule_time(self, item, now_time):
        """
        Judging given item whether start at now time
        :now_time: given time stamp
        :return:True Or False
        """
        if item['valid_status'] is False:
            return

        if item["schedule__data_schedule_type"] not in [self.SCHEDULE_GET_NORMALLY,
                                                        self.SCHEDULE_SPECIALLY]:
            item['valid_status'] = True
            return
        """
        collection data normally
        """
        if item["schedule__data_schedule_type"] == self.SCHEDULE_GET_NORMALLY:
            item['valid_status'] = True
            return True

        """
          collection data periodically
          """
        if item["schedule__data_schedule_type"] == self.SCHEDULE_SPECIALLY:
            """
            filter week
            """
            weeks = str(item["schedule__data_schedule_time"].split(self.SCHEDULE_DATE_SPLIT)[0]).split(
                self.SCHEDULE_WEEKS_SPLIT)
            week_status = self.__check_week(now_time, weeks)
            if week_status:
                now_date = time.localtime(now_time)
                tmp_start = time.strptime(str(item["schedule__data_schedule_time"].split(
                    self.SCHEDULE_DATE_SPLIT)[1])
                                          .split(self.SCHEDULE_SPLIT)[0], "%H:%M")
                tmp_end = time.strptime(str(item["schedule__data_schedule_time"]
                                            .split(self.SCHEDULE_DATE_SPLIT)[1]).split("-")[1], "%H:%M")
                now = time.strptime(str(str(now_date.tm_hour) + ":" + str(now_date.tm_min)), "%H:%M")
                status = self.__check_date_range(tmp_start, tmp_end, now)
                item['valid_status'] = status
                return status
            item['valid_status'] = False
            return item

    def __check_period_time(self, item, now_time):
        """
        0: open valid period type
        1: close valid period type
        """
        if item['schedule__valid_period_type'] == self.OPEN_VALID_PERIOD_TYPE:
            item_valid_period_time = self.__translate_valid_period_date((item['schedule__start_period_time'],
                                                                         item['schedule__end_period_time']))
            item['valid_status'] = self.__check_date_range(item_valid_period_time[0], item_valid_period_time[1],
                                                           now_time)
        else:
            item['valid_status'] = True
        return

    @staticmethod
    def __check_week(now_time, weeks):
        """
        Judging given now time is given week
        :param now_time: time stamp
        :param weeks:week
        :return:True Or False
        """
        now_date = time.localtime(now_time)
        if str(now_date.tm_wday + 1) in weeks:
            return True
        return False

    @staticmethod
    def __check_date_range(start_time, end_time, now_time):
        """
        Judging given time whether in date range
        :param start_time: start date time stamp
        :param end_time: end date time stamp
        :param now_time: now date time stamp
        :return: True or False
        """
        if start_time <= now_time <= end_time:
            return True
        return False

    def __translate_valid_period_date(self, given_date):
        """
        translate given date to time stamp
        :param given_date: Schedule's valid period time
        :return:time stamp
        """
        start_date = given_date[0]
        end_date = given_date[1]
        start_time_stamp = time.strptime(start_date, self.VALID_DATE_FORMAT)
        end_time_stamp = time.strptime(end_date, self.VALID_DATE_FORMAT)
        return int(time.mktime(start_time_stamp)), int(time.mktime(end_time_stamp))


class GetValidItem(CollectionValidate):
    def __init__(self):
        super(GetValidItem, self).__init__()

    def valid(self, now_time):
        self.items = self.get_items(None)
        return self.valid_items(now_time)


class GetValidItemByPolicy(CollectionValidate):
    def __init__(self):
        super(GetValidItemByPolicy, self).__init__()

    def valid(self, now_time, policy_id):
        self.items = self.get_items(None)
        self.valid_items(now_time)
        return len([item for item in self.items if item['valid_status'] and item['coll_policy_id'] == policy_id])


class GetValidItemByPolicyGroup(CollectionValidate):
    def __init__(self):
        super(GetValidItemByPolicyGroup, self).__init__()

    def valid(self, now_time, policy_group):
        self.items = self.get_items(None)
        self.valid_items(now_time)
        return len([item for item in self.items if item['valid_status'] and
                    item['policys_groups__policy_group_id'] == policy_group])


if __name__ == "__main__":
    test_instance = GetValidItemByPolicy()
    test_instance.valid(int(time.time()), 14)
    test_instance = GetValidItemByPolicyGroup()
    test_instance.valid(int(time.time()), 14)
    # for i in test_instance.items:
    #     print i
    # pass
    test_instance = GetValidItem()
    valid_items = test_instance.valid_items(int(time.time()))
    for i in test_instance.items:
        print i





