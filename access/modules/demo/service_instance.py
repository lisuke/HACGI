from access.dbus.module_service_interface import ServiceABC
import os


def on(iface):
    iface.is_on = True
    print("press on")


def off(iface):
    iface.is_on = False
    print("press off")


def valueChanged(iface, value):
    print("valueChanged, current value is {}.".format(value))


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
        self.RegisterMethodToInterface(
            "switch_interface", "on", on)
        self.RegisterMethodToInterface(
            "switch_interface", "off", off)
        self.RegisterMethodToInterface(
            "range_selector", "valueChanged", valueChanged)
