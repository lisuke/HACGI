from abc import ABCMeta, abstractmethod, abstractproperty
from base.abstract.service_type_interface import ServiceTypeInterface
from base.abstract.control_interface.switch_interface import ControlABC as SwitchABC


class ControlTypeABC(ServiceTypeInterface):
    """docstring for ControlTypeABC"""

    def __init__(self, *args, **kwargs):
        super(ControlTypeABC, self).__init__(*args, **kwargs)

        self.switch_abc = SwitchABC()
        self.RegisterInterface('switch_abc', self.switch_abc)
