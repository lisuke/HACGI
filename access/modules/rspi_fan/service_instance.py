from access.dbus.module_service_interface import ServiceABC
import os

current_value = 50
is_on = True

def on(iface):
    iface.is_on = True
    print("press on")
    global is_on
    is_on = True
    iface.p.start(current_value)


def off(iface):
    iface.is_on = False
    print("press off")
    global is_on
    is_on = False
    iface.p.stop()


def valueChanged(iface, value):
    current_value = value
    global is_on
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
