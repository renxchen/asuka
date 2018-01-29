# __author__ = 'haonchen'
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.smi import builder, view
from pysnmp.entity import engine
from pysnmp.entity.rfc3413 import context
from pysnmp.smi.error import SmiError, PySnmpError
import re
import os
import time
import logging


class SnmpTimeout(SmiError):
    def __init__(self):
        self.message = "No SNMP response received before timeout"

    def __str__(self):
        return self.message


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


class SNMP(object):
    def __init__(self, ip, community, logger,
                 port, timeout, retries,
                 non_repeaters, max_repetitions,
                 model_version=1, is_translate=False):
        self._syntax = {
            0: {
                '0x02': 'INTEGER',
                '0x04': 'OCTET STRING',
                '0x05': 'NULL',
                '0x06': 'OBJECT IDENTIFIER',
                '0x40': 'IpAddress',
                '0x41': 'Counter',
                '0x42': 'Gauge',
                '0x43': 'TimeTicks',
                '0x44': 'Opaque'
            },
            1: {
                '0x02': 'Integer32',
                '0x04': 'OCTET STRING',
                '0x05': 'NULL',
                '0x06': 'OBJECT IDENTIFIER',
                '0x40': 'IpAddress',
                '0x41': 'Counter32',
                '0x42': 'Gauge32',
                '0x43': 'TimeTicks',
                '0x44': 'Opaque',
                '0x45': 'NsapAddress',
                '0x46': 'Counter64',
                '0x47': 'UInteger32'
            }
        }

        self._errsyntax = {
            '0x80': 'NoSuchObject',
            '0x81': 'NoSuchInstance'
        }
        self.is_translate = is_translate
        self.maxvars = 20
        self._model = model_version

        _dirs, _resources = self.__read_import_resource()
        self._snmp_engine = engine.SnmpEngine()
        self._contxt = context.SnmpContext(self._snmp_engine)
        self._mib_builder = self._contxt.getMibInstrum().getMibBuilder()
        self.mib_view_controller = view.MibViewController(self._mib_builder)
        self._mib_builder.addMibSources(builder.DirMibSource(_dirs))
        self.logger = logger
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.non_repeaters = non_repeaters
        self.max_repetitions = max_repetitions
        self.cmd_gen = cmdgen.CommandGenerator()
        self.community_data = cmdgen.CommunityData(community, mpModel=self._model)
        self.transport_target = cmdgen.UdpTransportTarget((ip, port),
                                                          timeout=timeout,
                                                          retries=retries)

    def _GetValueAndType(self, val):
        """[PRIVATE] create MIB-value result
        :param:val: MIB-value-object
        :return: list(value, type)
        """
        try:
            _val = val.prettyPrint()
            # create syntax-key
            _tags = val.getTagMap().getPosMap().keys()[0][0]
            _tagD = 0
            for x in _tags:
                _tagD += x
            _tagH = '0x' + str('0' + '%x' % (_tagD,))[-2:]
            _syn = self._syntax.get(self._model)
            if not _syn:
                raise Exception('No Syntax Version')
            _type = _syn.get(_tagH)
            _kls = val.__class__.__name__
            # not in syntax type -> substitute className
            if not _type:
                if _tagH in self._errsyntax:
                    _val = False
                _type = _kls
            # class DisplayString == STRING(0x04)?
            if _tagH == '0x04' and _kls.lower() == 'displaystring':
                _type = 'STRING'
            return [_val, _type]
        except Exception as e:
            raise e

    def _GetValueDict(self, var):
        """[PRIVATE] create dictionary result
        :param:var: pysnmp returned varBind
        :return: dictionary(MIB-name: [MIB-value, MIB-type])
        """
        _var = [x for x in var]
        try:
            _val = self._GetValueAndType(_var[1])
        except Exception as e:
            # print e
            _val = [False, 'Exception']
        _key = _var[0].prettyPrint()
        return {_key: _val}

    def __read_import_resource(self):
        _resources = []
        _base_path = os.path.dirname(os.path.abspath(__file__))
        _dirs = os.path.join(_base_path, "mibs")
        _resources = [os.path.splitext(files)[0] for files in os.listdir(_dirs)]
        return _dirs, _resources

    def __load_resource(self, _resources):
        for resource in _resources:
            try:
                self._mib_builder.loadModules(str(resource))
            except SmiError as e:
                if "already exported" in str(e):
                    continue
                raise

    def __node_for_tuple(self, tpl):
        _tmp = [str(x) for x in tpl]
        try:
            if len(_tmp) == 1:
                _mibN, = self._mib_builder.imporSymbols(*_tmp)
                _ids = tuple()
            else:
                _symbols = _tmp[0:2]
                _ids = tuple([int(x) for x in _tmp[2:]])
                _mibN, = self._mib_builder.importSymbols(*_symbols)
            _ret = _mibN.getName() + _ids
        except Exception, e:
            _ret = tuple(_tmp)
        return _ret

    def __node_id(self, oid):
        _tmp = tuple(re.split(r'::|\.', oid))
        return self.__node_for_tuple(_tmp)

    def __get_oid(self, args):
        _ret = tuple()
        if len(args) == 1:
            args = args[0]
            if '::' in args:
                _ret = self.__node_id(args)
            elif re.search(r'[a-zA-Z]', args):
                _ret = self.__node_for_tuple(tuple([args]))
            else:
                try:
                    _ret = tuple([int(x) for x in args.strip('.').split('.')])
                except:
                    _ret = self.__node_for_tuple(tuple([args]))
        else:
            _ret = self.__node_for_tuple(args)
        return _ret

    def get_oid(self, args):
        if len(args) > 1:
            return [self.__get_oid((oid,)) for oid in args]
        else:
            return [self.__get_oid((oid,)) for oid in args]

    def walk(self, *oid_str):
        cmd_gen = self.cmd_gen
        error_indication, error_status, error_index, var_binds = cmd_gen.nextCmd(
            self.community_data,
            self.transport_target,
            *oid_str
        )
        if error_indication:
            self.logger.error('%s: %s', error_indication, self.ip)
            if str(error_indication).find("response received before timeout") > 0:
                raise SnmpTimeout
            raise PySnmpError(error_indication)
        else:
            if error_status:
                error_msg = error_status.prettyPrint()
                self.logger.error('%s: %s at %s', self.ip, error_msg,
                                  error_index and var_binds[-1][int(error_index) - 1] or '?')
                raise PySnmpError(error_msg)
            else:
                output = []
                for val in var_binds:
                    value = self._GetValueDict(val) if self.is_translate else str(val[1].prettyPrint())
                    output.append(dict(oid=str(val[0]),
                                       value=value,
                                       status="success"))
                return output

    def bulk_walk(self, *oid_str):
        cmd_gen = self.cmd_gen
        error_indication, error_status, error_index, var_binds = cmd_gen.bulkCmd(
            self.community_data,
            self.transport_target,
            *oid_str
        )
        if error_indication:
            self.logger.error('%s: %s', error_indication, self.ip)
            if str(error_indication).find("response received before timeout") > 0:
                raise SnmpTimeout
            raise PySnmpError(error_indication)
        else:
            if error_status:
                error_msg = error_status.prettyPrint()
                self.logger.error('%s: %s at %s', self.ip, error_msg,
                                  error_index and var_binds[-1][int(error_index) - 1] or '?')
                raise PySnmpError(error_msg)
            else:
                output = []
                for val in var_binds:
                    value = self._GetValueDict(val) if self.is_translate else str(val[1].prettyPrint())
                    output.append(dict(oid=str(val[0]),
                                       value=value,
                                       status="success"))
                return output

    def get(self, *oid_list):
        cmd_gen = self.cmd_gen
        exception_msg = None
        error_indication = None
        error_status = None
        error_index = None
        var_binds = None
        try:
            error_indication, error_status, error_index, var_binds = cmd_gen.getCmd(
                self.community_data,
                self.transport_target,
                *oid_list
            )
        except Exception, e:
            exception_msg = str(e)
        return error_indication, error_status, error_index, var_binds, exception_msg

    def translate(self, value):
        value = self._GetValueDict(value) if self.is_translate else str(value[1].prettyPrint())
        # value = str(value[1].prettyPrint())
        return value

    def bulk_get(self, *oid_str):
        oid_str = self.get_oid(*oid_str)
        output = []
        cmd_gen = self.cmd_gen
        if len(oid_str) > self.maxvars:
            _oid_splits = chunks(oid_str, self.maxvars)
        else:
            _oid_splits = [oid_str]

        for _oid_strs in _oid_splits:
            exception_msg, error_indication, error_status = "", "", ""
            try:
                error_indication, error_status, error_index, var_binds = cmd_gen.getCmd(
                    self.community_data,
                    self.transport_target,
                    *_oid_strs
                )
            except Exception, e:
                exception_msg = str(e)

            if error_indication or error_status or exception_msg:
                if len(_oid_strs) > 1:
                    for _oid_str in _oid_strs:

                        _error_indication, _error_status, _exception_msg = "", "", ""
                        try:
                            _error_indication, _error_status, _error_index, _var_binds = cmd_gen.getCmd(
                                self.community_data,
                                self.transport_target,
                                _oid_str
                            )
                        except Exception, e:
                            _exception_msg = str(e)

                        if _exception_msg:
                            output.append(dict(oid=_oid_str,
                                               value="",
                                               message=str(_exception_msg)))

                        elif _error_indication:
                            self.logger.error('%s: %s', _error_indication, self.ip)
                            output.append(dict(oid=_oid_str,
                                               value="",
                                               message=str(_error_indication)))
                        elif _error_status:

                            error_msg = _error_status.prettyPrint()
                            self.logger.error('%s: %s at %s', self.ip, error_msg,
                                              _error_index and _var_binds[-1][int(_error_index) - 1] or '?')
                            output.append(dict(oid=_oid_str,
                                               value="",
                                               message=str(error_msg)))
                        else:
                            for value in _var_binds:
                                output.append(dict(oid=str(value[0]),
                                                   value=self.translate(value)))
                else:
                    if exception_msg:
                        output.append(dict(oid=_oid_strs[0],
                                           value="",
                                           message=str(exception_msg)))

                    elif error_indication:
                        self.logger.error('%s: %s', error_indication, self.ip)
                        output.append(dict(oid=_oid_strs[0],
                                           value="",
                                           message=str(error_indication)))
                    elif error_status:
                        error_msg = error_status.prettyPrint()
                        self.logger.error('%s: %s at %s', self.ip, error_msg,
                                          error_index and var_binds[-1][int(error_index) - 1] or '?')
                        output.append(dict(oid=_oid_strs[0],
                                           value="",
                                           message=str(error_msg)))


            else:
                for value in var_binds:
                    output.append(dict(oid=str(value[0]),
                                       value=self.translate(value)))

        return dict(status='success',
                    message='',
                    output=output)


# with open("oids", "rb") as f:
#     oids = f.read().split("\r\n")
# oids = filter(lambda x: len(x) > 0, oids)
# start_time = time.time()
# test = SNMP("10.71.244.135", "cisco", logging, 161, 10, 1, 1, 1, model_version=1, is_translate=True)
# result = test.bulk_get(oids)
# for i, v in enumerate(result['output']):
#     print i, v
# end_time = time.time()
# print end_time - start_time
