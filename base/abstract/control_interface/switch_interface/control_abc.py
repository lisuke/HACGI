from abc import ABCMeta, abstractmethod, abstractproperty
from base.abstract.service_type_interface import ControlInterface


class ControlABC(ControlInterface):
    """docstring for ControlABC"""

    def __init__(self, *args, **kwargs):
        super(ControlABC, self).__init__(*args, **kwargs)
        self.DeclareMethod("on")
        self.DeclareMethod("off")
