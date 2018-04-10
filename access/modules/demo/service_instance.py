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
        super(ServiceInstance, self).Init()
