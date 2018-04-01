from abc import ABCMeta, abstractmethod, abstractproperty
from base.abstract.service_type_interface import ControlInterface


class SwitchInterface(ControlInterface):
    """docstring for SwitchInterface"""

    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass
