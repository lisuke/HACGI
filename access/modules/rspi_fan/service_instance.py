from access.dbus.module_service_interface import ServiceABC
import os


def on(iface):
    iface.is_on = True
    print("press on")
    self.GPIO.output(35, 1)


def off(iface):
    iface.is_on = False
    print("press off")
    self.GPIO.output(35, 0)


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

        import RPi.GPIO as GPIO
        self.GPIO = GPIO

        self.GPIO.setmode(GPIO.BOARD)
        self.GPIO.setup(35, GPIO.OUT)
