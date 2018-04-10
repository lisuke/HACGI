from abc import ABCMeta, abstractmethod, abstractproperty
from base.abstract.service_type_interface import ControlInterface


class ControlABC(ControlInterface):
    """docstring for ControlABC"""

    def __init__(self, *args, **kwargs):
        super(ControlABC, self).__init__(*args, **kwargs)
        self.DeclareMethod("setRange")
        self.DeclareMethod("getRange")
        self.DeclareMethod("setValue")
        self.DeclareMethod("getValue")
        self.DeclareMethod("inc")
        self.DeclareMethod("dec")
        self.DeclareMethod("valueChanged")

        self.RegisterMethod("setRange", self.setRange)
        self.RegisterMethod("getRange", self.getRange)
        self.RegisterMethod("setValue", self.setValue)
        self.RegisterMethod("getValue", self.getValue)
        self.RegisterMethod("inc", self.__increment__)
        self.RegisterMethod("dec", self.__decrement__)

    def setRange(self, value_range):
        self.min_value = value_range[0]
        self.max_value = value_range[1]

    def getRange(self):
        return (min_value, max_value)

    def setValue(self, value):
        self.current_value = value
        self.valueChanged(self.current_value)

    def getValue(self):
        return self.current_value

    def __increment__(self):
        self.current_value = self.current_value + 1
        self.valueChanged(self.current_value)

    def __decrement__(self):
        self.current_value = self.current_value - 1
        self.valueChanged(self.current_value)
