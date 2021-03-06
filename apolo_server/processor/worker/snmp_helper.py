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
                 port, timeout, retries,device_log_info,
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

        self._errinfo=[
            "No Such Instance",
            "No Such Object"

        ]

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
        self.device_log_info = device_log_info
        #self.non_repeaters = non_repeaters
        #self.max_repetitions = max_repetitions
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
        try:
            _resources = []
            _base_path = os.path.dirname(os.path.abspath(__file__))
            _dirs = os.path.join(_base_path, "mibs")
            _resources = [os.path.splitext(files)[0] for files in os.listdir(_dirs)]
        except:
            return "",""
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
    def translate(self, value):
        status = "success"
        message = ""
        if self.is_translate:
            value = self._GetValueDict(value) 
            for key in value:
                if value[key][1] in ["Exception","NoSuchObject","NoSuchInstance"]:
                    status = "fail"
                    message = value[key][1]
                    break
        else:
            value = str(value[1].prettyPrint())
            for err_reg in self._errinfo:
                if re.search("^"+err_reg,value,re.IGNORECASE) is not None:
                    status = "fail"
                    message = value
                    break
        return value,status,message

    def bulk_get(self, oids):
        #print oids
        _oid_strs = self.get_oid(oids)
        output = []
        cmd_gen = self.cmd_gen

        exception_msg, error_indication, error_status = "", "", ""
        try:
           
            error_indication, error_status, error_index, var_binds = cmd_gen.getCmd(
                self.community_data,
                self.transport_target,
                *_oid_strs
            )
           
        except Exception, e:
            exception_msg = str(e)

        # if error_indication:
        if error_indication and str(error_indication).find("response received before timeout") > 0:
                raise Exception(str(error_indication))
 
        if error_indication or error_status or exception_msg:
            if len(_oid_strs) > 1:
                for index,_oid_str in enumerate(_oid_strs):
                    origin_oid = oids[index]                        
                    _error_indication, _error_status, _exception_msg = "", "", ""
                    try:
                        _error_indication, _error_status, _error_index, _var_binds = cmd_gen.getCmd(
                            self.community_data,
                            self.transport_target,
                            _oid_str
                        )
                    except Exception, e:
                        _exception_msg = str(e)

                    err_msg = ""
                    if _exception_msg:
                        err_msg = "%s OID:%s Error Info:%s"%(self.device_log_info,origin_oid,str(_exception_msg))
                        output.append(dict( status="fail",
                                            origin_oid=origin_oid,
                                            oid=_oid_str,
                                            value="",
                                            message=str(_exception_msg)))

                    elif _error_indication:
                        err_msg = "%s OID:%s Error Info:%s"%(self.device_log_info,origin_oid,str(_error_indication))
                        output.append(dict(status="fail",
                                            origin_oid=origin_oid,
                                            oid=_oid_str,
                                            value="",
                                            message=str(_error_indication)))
                    elif _error_status:
                        error_msg = _error_status.prettyPrint()
                        error_msg = '%s: OID:%s Error Info:%s at %s' % (self.device_log_info,origin_oid,error_msg,_error_index and _var_binds[-1][int(_error_index) - 1] or '?')
                        output.append(dict(
                                            status="fail",
                                            origin_oid=origin_oid,
                                            oid=_oid_str,
                                            value="",
                                            message=str(error_msg)))
                    else:
                        for value in _var_binds:
                            _value,_status,_message = self.translate(value)
                            output.append(dict(status=_status,
                                                origin_oid=origin_oid,
                                                oid=str(value[0]),
                                                value=_value,
                                                message = _message
                                                ))
                    
                    if error_msg:
                        self.logger.error(err_msg)
            else:
                err_msg = ""
                if exception_msg:
                    err_msg = "%s OID:%s Error Info:%s"%(self.device_log_info,oids[0],str(exception_msg))
                    output.append(dict(status="fail",
                                        origin_oid=oids[0],
                                        oid=_oid_strs[0],
                                        value="",
                                        message=str(exception_msg)))

                elif error_indication:
                    err_msg = "%s OID:%s Error Info:%s"%(self.device_log_info,oids[0],str(error_indication))
                    #self.logger.error('%s: %s', error_indication, self.ip)
                    output.append(dict(
                                        status="fail",
                                        origin_oid=oids[0],
                                        oid=_oid_strs[0],
                                        value="",
                                        message=str(error_indication)))
                elif error_status:
                    error_msg = error_status.prettyPrint()
                    error_msg = '%s: OID:%s Error Info:%s at %s' % (self.device_log_info,oids[0],error_msg,error_index and var_binds[-1][int(error_index) - 1] or '?')
                    output.append(dict(status="fail",
                                        origin_oid=oids[0],
                                        oid=_oid_strs[0],
                                        value="",
                                        message=str(error_msg)))
                
                if err_msg:
                    self.logger.error(err_msg)
        else:
            for index,value in enumerate(var_binds):
                _value,_status,_message = self.translate(value)                                 
                output.append(dict( status=_status,
                                    origin_oid=oids[index],
                                    oid=str(value[0]),
                                    value=_value,
                                    message=_message
                                    ))

        return dict(status='success',
                    message='',
                    output=output)

if __name__ == "__main__":

    log_pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_pattern)
  
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger = logging.getLogger("SNMP")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.propagate = False
    device_log_info="Device ID: 1000,IP: 10.71.244.135,HostName: crs1000"
    #logger.info('%s for %s started', operate.upper(), ip)

    worker = SNMP(  "10.71.244.135",
                    "cisco",
                    logger=logger,
                    port=161,
                    timeout=5,
                    retries=2,
                    device_log_info=device_log_info,
                    model_version=1,
                    is_translate=True
                    )
    try:
        import traceback
        import json
        #oids = ["1.3.6.1.2.1.1.2.0"]
        maxvars = 20
        #if operate == 'bulk_get':
        snmp_fun = worker.bulk_get
        with open("/Users/yihli/Desktop/projects/apolo/apolo_server/processor/worker/oids") as f:
            oids = [line.strip() for line in f.readlines()]
             #sys.exit()
        
        if len(oids) > maxvars:
            _oid_splits = chunks(oids, maxvars)
        else:
            _oid_splits = [oids]
        fw = open("/Users/yihli/Desktop/projects/apolo/apolo_server/processor/worker/result","w")
        for _oids in _oid_splits:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            clock = time.time()
            result = snmp_fun(_oids)
            
            #for data in result["output"]:
            #   data["item_ids"] = oid_dict[data["origin_oid"]]
            
            result.update(dict(result_type="element_result",  timestamp=timestamp, clock="%f" % clock))
            print result
            #self.zmq_push.send(json.dumps(result))
            fw.write(json.dumps(result,indent=2))

        fw.close()
        #logger.info('%s for %s finished', operate.upper(), ip)
        #result = snmp_fun(tuple(oids))
        status = "success"
        message = ""
    except Exception as e:  
        traceback.format_exc()          
        status = 'fail'
        message = str(e)
        logger.error("%s %s"%(device_log_info, str(e)))

