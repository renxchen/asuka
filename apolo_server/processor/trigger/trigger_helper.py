from apolo_server.processor.constants import TriggerConstants
from apolo_server.processor.db_units.db_helper import TriggerDbHelp
from apolo_server.processor.trigger.function_helper import Max, Min, Avg, Hex2Dec, Last, LastRange, handle_expression, \
    _create_item
from apolo_server.processor.units import FunctionException


class TriggerHelp(object):
    def __init__(self, items, logger):
        self.logger = logger
        self.items = items

    def trigger(self, task_timestamp):
        triggers = TriggerDbHelp.get_triggers_by_item_id(self.items.keys())
        events = []
        items = self.items
        MAX, MIN, AVG, HEX2DEC, LAST, LASTRANGE = Max(), Min(), Avg(), Hex2Dec(), Last(), LastRange()
        for trigger in triggers:
            trigger.expression = handle_expression(trigger.expression)
            try:
                trigger_status = eval(trigger.expression)
            except FunctionException, e:
                self.logger.error(str(e))
            events.append([trigger.trigger, trigger_status, task_timestamp])
        self.save_event(events)

    def save_event(self, events):
        """
        :param events:
        :return:Null
        """
        """
        trigger_status 0:normal
        trigger_status 1:trigger
        """
        tmp = []
        for event in events:
            trigger_instance = event[0]
            instance = TriggerDbHelp.get_latest_event(TriggerConstants.TRIGGER_EVENT_SOURCE, trigger_instance.trigger_id)
            if len(instance) == 0:
                latest_number = 0
            else:
                latest_number = instance[len(instance) - 1]['number']
            if event[1]:
                latest_number = 0
                value = TriggerConstants.NORMAL_VALUE
            else:
                latest_number += 1
                value = TriggerConstants.TRIGGER_VALUE
            if latest_number >= trigger_instance.trigger_limit_nums:
                latest_number = 0
            tmp.append(
                [TriggerConstants.TRIGGER_EVENT_SOURCE, trigger_instance.trigger_id, latest_number, event[2], value])
        TriggerDbHelp.save_events(tmp)