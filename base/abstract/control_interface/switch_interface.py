from abc import ABCMeta, abstractmethod, abstractproperty


class SwitchInterface(object):
    """docstring for SwitchInterface"""

    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass
