import json

__author__ = 'zhutong'

LOCAL_FILE = 'device_credential.json'


def _filter_device(device, q):
    if q in device.get('hostname', '').lower():
        return True
    if q in device['platform'].lower():
        return True
    if q in ' '.join(device.get('tag', [''])).lower():
        return True
    return False

class CredentialManager(object):
    """
    A very simple credential manager
    """
    platforms = ['ios', 'nxos', 'asa', 'f5', 'hw', 'h3c', 'juniper', 'brocade']
    common = dict(username='cisco',
                  password='cisco',
                  community='public',
                  method='telnet',
                  tag='',
                  platform='ios')
    device_dict = {}
    device_list = []

    def __init__(self):
        self.load()

    def query(self, q):
        if not q:
            devices = self.device_list
        else:
            if '|' in q and '&' in q:
                return dict(status='error',
                            message='Not support "&"" and "|"" in one query',
                            devices=[])
            if '|' in q:
                devices = []
                for s in q.split('|'):
                    ds = [d for d in self.device_list if _filter_device(d, s)]
                    devices.extend(ds)
            elif '&' in q:
                devices = self.device_list
                for s in q.split('&'):
                    devices = [d for d in devices if _filter_device(d, s)]
            else:
                devices = [d for d in self.device_list if _filter_device(d, q)]
        return dict(status='ok',
                    devices=devices)
        
    def create(self, **kwargs):
        if 'platform' in kwargs:
            platform = kwargs['platform']
            if platform not in self.platforms:
                return dict(status='error',
                            err_msg='Not support platform')

        if 'ip' not in kwargs:
            return dict(status='error',
                        err_msg='No ip info')

        ip = kwargs['ip']
        if self.device_dict.get(ip):
            return dict(status='error',
                        err_msg='Device already in db. Using update instead.')

        device = dict(**kwargs)
        self.device_dict[ip] = device
        if 'hostname' in device:
            self.device_dict[device['hostname']] = device
        
        self.device_list.append(device)
        return dict(status='ok')

    def create_m(self, device_info_list):
        for device_info in device_info_list:
            self.create(**device_info)
        return dict(status='ok')

    def update(self, device_id, **kwargs):
        device = self.device_dict.get(device_id)
        if not device:
            return self.create(**kwargs)

        if 'platform' in kwargs:
            platform = kwargs['platform']
            if platform not in self.platforms:
                return dict(status='error',
                            err_msg='Not supported platform')

        device.update(**kwargs)
        return dict(status='ok')

    def update_m(self, device_info_list):
        for device_info in device_info_list:
            device_id = device_info['hostname']
            self.update(device_id, **device_info)
        return dict(status='ok')

    def delete(self, device_id):
        device = self.device_dict.get(device_id)
        if device:
            ip = device['ip']
            hostname = device.get('hostname')
            if hostname:
                del self.device_dict[hostname]
            del self.device_dict[device['ip']]
            for d in self.device_list:
                if d['ip'] == ip:
                    self.device_list.remove(d)
                    break
            return dict(status='ok')
        else:
            return dict(status='error',
                        err_msg='Device not found')

    def get(self, device_id):
        params = self.device_dict.get(device_id)
        if not params:
            return dict(status='error',
                        err_msg='Device not found')
        device = self.common.copy()
        device.update(params)
        return dict(status='ok',
                    device_info=device)

    def get_all(self):
        all_device = {}
        for device_id in self.device_dict:
            params = self.device_dict.get(device_id)
            device = self.common.copy()
            device.update(params)
            all_device[device_id] = device
        return dict(status='ok',
                    device_info=all_device)

    def get_common(self):
        return dict(status='ok',
                    common=self.common)

    def set_common(self, kwargs):
        self.common.update(**kwargs)
        return dict(status='ok')

    def save(self, filename=LOCAL_FILE):
        try:
            devices=sorted((self.device_list))
            data = dict(common=self.common, devices=devices)
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return dict(status='ok')
        except Exception as e:
            print e.message
            return dict(status='error',
                        err_msg='Save device credential failed.')

    def load(self, filename=LOCAL_FILE):
        try:
            with open(filename) as f:
                data = json.load(f)
                self.common.update(data['common'])
                self.create_m(data['devices'])
            return dict(status='ok')
        except Exception as e:
            print e.message
            return dict(status='error',
                        err_msg='Load device credential failed.')
