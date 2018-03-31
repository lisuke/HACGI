from access.dbus.module_service_interface import ServiceABC
import os


class ServiceInstance(ServiceABC):

    @property
    def config_file_path(self):
        return os.path.split(os.path.realpath(__file__))[0] + '/service.conf'

    @property
    def config_section(self):
        return "CurrentConfig"

    # #############################

    def Init(self):
        pass

    def HoldInterFace(self, InterfaceName, ret_has_own):
        pass

    def ControlInterFace(self, InterfaceName, arg_JSON_Value):
        pass
