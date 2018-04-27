from abc import ABCMeta, abstractmethod, abstractproperty
from base.abstract.service_type_interface import ControlInterface


def __toJson__(iface):
    ret = ""
    if iface.is_on:
        ret = {"is_on": True}
    else:
        ret = {"is_on": False}
    return ret


class ControlABC(ControlInterface):
    """docstring for ControlABC"""

    def __init__(self, *args, **kwargs):
        super(ControlABC, self).__init__(*args, **kwargs)
        self.DeclareMethod("on")
        self.DeclareMethod("off")
        self.RegisterMethod("__toJson__", __toJson__)
        self.is_on = False
