# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import time
from django.db import models
app_label = "db_units"

class User(models.Model):
    name = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=32, blank=True)
    token = models.CharField(max_length=500, blank=True)
    mail = models.CharField(max_length=200, blank=True)


class Actions(models.Model):
    action_id = models.AutoField(primary_key=True)
    action_type = models.CharField(max_length=255, blank=True, null=True)
    action_name = models.CharField(max_length=255, blank=True, null=True)
    snmp_version = models.CharField(max_length=255, blank=True, null=True)
    snmp_oid = models.CharField(max_length=255, blank=True, null=True)
    community = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    command = models.CharField(max_length=255, blank=True, null=True)
    agent_address = models.CharField(max_length=255, blank=True, null=True)
    oid = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    param = models.CharField(max_length=255, blank=True, null=True)
    script_path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    trigger = models.ForeignKey('Triggers', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'actions'


class CollPolicy(models.Model):
    coll_policy_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    cli_command = models.CharField(max_length=256, blank=True, null=True)
    cli_command_result = models.TextField(blank=True, null=True)
    desc = models.CharField(max_length=2000, blank=True, null=True)
    policy_type = models.IntegerField(blank=True, null=True)
    snmp_oid = models.CharField(max_length=256, blank=True, null=True)
    history = models.CharField(max_length=255, blank=True, null=True)
    value_type = models.IntegerField(blank=True, null=True)
    ostype = models.ForeignKey('Ostype', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'coll_policy'

    @property
    def ostype_name(self):
        return self.ostype.name


class CollPolicyCliRule(models.Model):
    ruleid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    key_str = models.CharField(max_length=30, blank=True, null=True)
    mark_string = models.CharField(max_length=256, blank=True, null=True)
    split_char = models.CharField(max_length=256, blank=True, null=True)
    extract_key = models.CharField(max_length=30, blank=True, null=True)
    x_offset = models.IntegerField(blank=True, null=True)
    y_offset = models.IntegerField(blank=True, null=True)
    line_nums = models.IntegerField(blank=True, null=True)
    rule_type = models.IntegerField(blank=True, null=True)
    end_mark_string = models.CharField(max_length=256, blank=True, null=True)
    start_line_num = models.IntegerField(blank=True, null=True)
    end_line_num = models.IntegerField(blank=True, null=True)
    desc = models.CharField(max_length=2000, blank=True, null=True)
    is_serial = models.IntegerField(blank=True, null=True)
    is_include = models.IntegerField(blank=True, null=True)
    command = models.CharField(max_length=256, blank=True, null=True)
    value_type = models.IntegerField(blank=True, null=True)
    coll_policy = models.ForeignKey(CollPolicy, models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'coll_policy_cli_rule'


class CollPolicyGroups(models.Model):
    policy_group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    desc = models.CharField(max_length=2000, blank=True, null=True)
    ostypeid = models.ForeignKey('Ostype', models.DO_NOTHING, db_column='ostypeid')

    class Meta:
        # managed = False
        db_table = 'coll_policy_groups'

    @property
    def ostype_name(self):
        return self.ostypeid.name


class CollPolicyRuleTree(models.Model):
    treeid = models.AutoField(primary_key=True)
    parent_tree_id = models.IntegerField(blank=True, null=True)
    is_leaf = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    rule_id_path = models.CharField(max_length=2000, blank=True, null=True)
    rule = models.ForeignKey(CollPolicyCliRule, models.DO_NOTHING)
    coll_policy = models.ForeignKey(CollPolicy, models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'coll_policy_rule_tree'


class DataTable(models.Model):
    table_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    descr = models.CharField(max_length=2000, blank=True, null=True)
    coll_policy = models.ForeignKey(CollPolicy, models.DO_NOTHING)
    groups = models.ForeignKey('Groups', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'data_table'


class DataTableItems(models.Model):
    data_table_items_id = models.AutoField(primary_key=True)
    table = models.ForeignKey(DataTable, models.DO_NOTHING)
    item = models.ForeignKey('Items', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'data_table_items'


class DevicesTmp(models.Model):
    operation_id = models.IntegerField(blank=True, null=True)
    device_id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    telnet_port = models.IntegerField(blank=True, null=True)
    snmp_port = models.IntegerField(blank=True, null=True)
    snmp_community = models.CharField(max_length=30, blank=True, null=True)
    snmp_version = models.CharField(max_length=5, blank=True, null=True)
    login_expect = models.CharField(max_length=1000, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    telnet_status = models.CharField(max_length=255, blank=True, null=True)
    snmp_status = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.CharField(max_length=255, blank=True, null=True)
    ostype = models.ForeignKey('Ostype', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'devices'


class Devices(models.Model):
    device_id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    telnet_port = models.IntegerField(blank=True, null=True)
    snmp_port = models.IntegerField(blank=True, null=True)
    snmp_community = models.CharField(max_length=30, blank=True, null=True)
    snmp_version = models.CharField(max_length=5, blank=True, null=True)
    login_expect = models.CharField(max_length=1000, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    telnet_status = models.CharField(max_length=255, blank=True, null=True)
    snmp_status = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.CharField(max_length=255, blank=True, null=True)
    ostype = models.ForeignKey('Ostype', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'devices'


class DevicesGroups(models.Model):
    devicegroup_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Devices, models.DO_NOTHING)
    group = models.ForeignKey('Groups', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'devices_groups'

    @property
    def group_name(self):
        return self.group.name


class Event(models.Model):
    event_id = models.IntegerField(primary_key=True)
    clock = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    objectid = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'event'


class Functions(models.Model):
    function_id = models.AutoField(primary_key=True)
    function = models.CharField(max_length=12, blank=True, null=True)
    parameter = models.CharField(max_length=255, blank=True, null=True)
    trigger_detail = models.ForeignKey('TriggerDetail', models.DO_NOTHING)
    item = models.ForeignKey('Items', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'functions'


class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    ostype = models.ForeignKey('Ostype', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'groups'


class HistoryCliFloat(models.Model):
    value = models.FloatField(blank=True, null=True)
    clock = models.IntegerField(blank=True, null=True)
    ns = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)
    block_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'history_cli_float'


class HistoryCliInt(models.Model):
    value = models.BigIntegerField(blank=True, null=True)
    clock = models.IntegerField(blank=True, null=True)
    ns = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)
    block_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'history_cli_int'


class HistoryCliStr(models.Model):
    clock = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    ns = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)
    block_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'history_cli_str'


class HistoryCliText(models.Model):
    clock = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    ns = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)
    block_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'history_cli_text'


class HistorySnmpFloat(models.Model):
    value = models.FloatField(blank=True, null=True)
    clock = models.IntegerField(blank=True, null=True)
    ns = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'history_snmp_float'


class HistorySnmpInt(models.Model):
    value = models.BigIntegerField(blank=True, null=True)
    clock = models.IntegerField(blank=True, null=True)
    ns = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'history_snmp_int'


class HistorySnmpStr(models.Model):
    clock = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    ns = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'history_snmp_str'


class HistorySnmpText(models.Model):
    clock = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    ns = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'history_snmp_text'


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    value_type = models.IntegerField(blank=True, null=True)
    item_type = models.IntegerField(blank=True, null=True)
    key_str = models.CharField(max_length=30, blank=True, null=True)
    # modify 1.17 add default value
    status = models.IntegerField(blank=True, null=True, default=1)
    # modify 1.17 add default value
    last_exec_time = models.IntegerField(blank=True, null=True, default=0)
    coll_policy = models.ForeignKey(CollPolicy, models.DO_NOTHING)
    coll_policy_rule_tree_treeid = models.ForeignKey(CollPolicyRuleTree, models.DO_NOTHING,
                                                     db_column='coll_policy_rule_tree_treeid',
                                                     blank=True, null=True)
    device = models.ForeignKey(Devices, models.DO_NOTHING)
    schedule = models.ForeignKey('Schedules', models.DO_NOTHING)
    # add 1.17
    # add 1.17
    policys_groups = models.ForeignKey('PolicysGroups', models.DO_NOTHING)

    #add 2.28 v1.5
    enable_status = models.IntegerField(blank=True, null=True)
    groups = models.ForeignKey(Groups, models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'items'


class Mapping(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    descr = models.CharField(max_length=2000, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    code_meaning = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'mapping'


class Ostype(models.Model):
    ostypeid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    log_fail_judges = models.CharField(max_length=2048, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    snmp_timeout = models.IntegerField(blank=True, null=True)
    telnet_timeout = models.IntegerField(blank=True, null=True)
    telnet_prompt = models.CharField(max_length=255, blank=True, null=True)
    start_default_commands = models.CharField(max_length=2048, blank=True, null=True)
    end_default_commands = models.CharField(max_length=2048, blank=True, null=True)
    desc = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'ostype'


class PolicysGroups(models.Model):
    policys_groups_id = models.AutoField(primary_key=True)
    exec_interval = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    history = models.CharField(max_length=255, blank=True, null=True)
    policy = models.ForeignKey(CollPolicy, models.DO_NOTHING)
    policy_group = models.ForeignKey(CollPolicyGroups, models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'policys_groups'

    @property
    def policy_name(self):
        return self.policy.name


class Schedules(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    valid_period_type = models.IntegerField(blank=True, null=True)
    data_schedule_type = models.IntegerField(blank=True, null=True)
    start_period_time = models.CharField(max_length=255, blank=True, null=True)
    end_period_time = models.CharField(max_length=255, blank=True, null=True)
    data_schedule_time = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    policy_group = models.ForeignKey(CollPolicyGroups, models.DO_NOTHING)
    device_group = models.ForeignKey(Groups, models.DO_NOTHING)
    ostype = models.ForeignKey(Ostype, models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'schedules'

    @property
    def policy_group_name(self):
        return self.policy_group.name

    @property
    def device_group_name(self):
        return self.device_group.name

    @property
    def ostype_name(self):
        return self.ostype.name

    @property
    def period_time(self):
        before = self.start_period_time.replace('@', ' ')
        after = self.end_period_time.replace('@', ' ')
        return str(before) + '~' + str(after)

    @property
    def schedules_is_valid(self):
        now_time = time.strftime('%Y-%m-%d@%H:%M:%S', time.localtime(time.time()))
        if self.valid_period_type == 0:
            return 1
        else:
            if self.start_period_time < now_time < self.end_period_time:
                return 1
            else:
                return 0



class TriggerDetail(models.Model):
    trigger_detail_id = models.AutoField(primary_key=True)
    expression = models.CharField(max_length=255, blank=True, null=True)
    descr = models.CharField(max_length=2000, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    trigger = models.ForeignKey('Triggers', models.DO_NOTHING)
    expression_view = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'trigger_detail'


class Triggers(models.Model):
    trigger_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    descr = models.CharField(max_length=2000, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    trigger_type = models.IntegerField(blank=True, null=True)
    trigger_limit_nums = models.IntegerField(blank=True, null=True)
    condition = models.IntegerField(blank=True, null=True)

    expression = models.CharField(max_length=255, blank=True, null=True)
    columnA = models.CharField(max_length=255, blank=True, null=True)
    columnB = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        # managed = False
        db_table = 'triggers'


if __name__ == "__main__":
    trigger = Triggers.objects.all()
    print trigger
