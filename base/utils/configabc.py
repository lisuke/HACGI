from abc import ABCMeta, abstractmethod, abstractproperty
from base.utils.config_utils import getConfig


class ConfigABC(metaclass=ABCMeta):
    """docstring for ConfigABC"""

    @abstractproperty
    def config_file_path():
        pass

    @abstractproperty
    def config_section():
        pass

    @property
    def config(self):
        if not hasattr(self, 'service_config'):
            self.service_config = getConfig(self.config_file_path)
            self.service_config.config_file_path = self.config_file_path
        return self.service_config

    def setKeyToSaveToConfig(self, key, value):
        if isinstance(key, str):
            print("module::" + self.ServiceName + " set:" + key, value)
            if not self.config.has_section(self.config_section):
                self.config.add_section(self.config_section)
            self.config.set(self.config_section, key, str(value))
            with open(self.config.config_file_path, "w") as fw:
                self.config.write(fw)

    def getKeyFromConfig(self, key, value_type, value_default):
        if type(value_type) == type:
            if self.config.has_option(self.config_section, key):
                value = self.config.get(self.config_section, key)
                if value_type == bool:
                    if value == str(True):
                        return True
                    else:
                        return False
                return value_type(value)
            else:
                return value_default
