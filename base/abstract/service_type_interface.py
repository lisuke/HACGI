from abc import ABCMeta, abstractmethod, abstractproperty


class ControlInterface(object):
    """docstring for ControlInterface"""

    pass


class ServiceTypeInterface(metaclass=ABCMeta):
    """docstring for ServiceTypeInterface"""

    @abstractproperty
    def Type(self):
        pass

    @abstractmethod
    def RegisterInterface(self, InterfaceName):
        pass

    @abstractmethod
    def HoldInterface(self, InterfaceName, ret_has_own):
        pass

    @abstractmethod
    def ControlInterface(self, InterfaceName, arg_JSON_Value):
        pass
