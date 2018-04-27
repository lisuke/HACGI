from abc import ABCMeta, abstractmethod, abstractproperty
from base.abstract.service_type_interface import ControlInterface


def __toJson__(iface):
    value = iface.__cbs__["getValue"](iface)
    print(value)
    return {"value": value}


def setRange(iface, value_range):
    iface.min_value = value_range[0]
    iface.max_value = value_range[1]


def getRange(iface):
    return (min_value, max_value)


def setValue(iface, value):
    iface.current_value = value
    iface.valueChanged(iface.current_value)


def getValue(iface):
    return iface.current_value


def __increment__(iface):
    iface.current_value = iface.current_value + 1
    iface.valueChanged(iface.current_value)


def __decrement__(iface):
    iface.current_value = iface.current_value - 1
    iface.valueChanged(iface.current_value)


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

        self.RegisterMethod("setRange", setRange)
        self.RegisterMethod("getRange", getRange)
        self.RegisterMethod("setValue", setValue)
        self.RegisterMethod("getValue", getValue)
        self.RegisterMethod("inc", __increment__)
        self.RegisterMethod("dec", __decrement__)
        self.RegisterMethod("__toJson__", __toJson__)

        self.min_value = 0
        self.max_value = 100
        self.current_value = 50

    def valueChanged(self, value):
        self.__cbs__["valueChanged"](self, value)
