from access.dbus.module_service_interface import ServiceABC
import os

is_on = False

def on(iface):
    iface.is_on = True
    print("press on")
    iface.GPIO.output(18, 1)
    is_on = True


def off(iface):
    iface.is_on = False
    print("press off")
    iface.GPIO.output(18, 0)
    iface.p.stop()
    is_on = False


def valueChanged(iface, value):
    if is_on == True:
        iface.p.start(value)
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

        switch_interface = self.TypeInterface.interfaces["switch_interface"]
        range_selector = self.TypeInterface.interfaces["range_selector"]
        
        import RPi.GPIO as GPIO
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.OUT)
        p = GPIO.PWM(18,100)
        switch_interface.GPIO = GPIO
        switch_interface.p = p
        range_selector.p = p
