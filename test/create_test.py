import sys
import os
import django
sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apolo_server.processor.db_units.settings")
django.setup()
from apolo_server.processor.db_units.models import Devices, Ostype


def __create_test_devices(numbers=1000):
    ip_range = range(101, 116)
    ip_len = len(ip_range)
    devices = []
    try:
        Ostype.objects.raw("INSERT INTO `ostype` (`ostypeid`,`name`,`log_fail_judges`,`status`,`snmp_timeout`,`telnet_timeout`,`telnet_prompt`,`start_default_commands`,`end_default_commands`,`desc`) VALUES (2,'asr9k',NULL,1,30,30,'#','terminal len 0;terminal pager 0',NULL,NULL);")
    except Exception, e:
        pass
    for i in range(numbers):
        ip = ip_range[i % ip_len]
        devices.append(
            Devices(
                hostname="Test%d" % i,
                ip=str(ip),
                telnet_status=0,
                snmp_status=0,
                snmp_community="cisco",
                login_expect="ssword:,cisco,>,enable,:,cisco123,#",
                status=1,
                ostype_id=2
            )
        )
    Devices.objects.bulk_create(devices)


if __name__ == "__main__":
    __create_test_devices()


