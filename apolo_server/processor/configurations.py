import os
import json


class Singleton(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            pass
        else:
            Singleton.instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.instance


class Configurations(Singleton):
    def __init__(self):
        self.base_folder = os.path.dirname(__file__)
        self.config = {}
        self.__load_configurations()

    def get_configuration(self, config_name):
        return self.config.get(config_name)

    @property
    def get_base_folder(self):
        return self.base_folder

    @property
    def show_all_configuration(self):
        return self.config

    def __set_configuration(self, config):
        self.config.update(config)
        self.__save_file()

    def __delete_configuration(self, key):
        if key in self.config:
            del self.config[key]
            self.__save_file()

    def __load_configurations(self):
        with open(os.path.join(self.base_folder, "configurations")) as f:
            self.config = json.loads(f.read())

    def __save_file(self):
        with open(os.path.join(self.base_folder, "configurations"), "w") as f:
            f.write(json.dumps(self.config))

    def _reload_configurations(self):
        self.__load_configurations()

    def _set_configurations(self, config):
        self.__set_configuration(config=config)

    def _delete_configurations(self, key):
        self.__delete_configuration(key)


if __name__ == "__main__":
    a = Configurations()

