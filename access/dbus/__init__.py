from pydbus import SessionBus
from gi.repository import GLib
from convergence.dbus.service_manager import ServiceManager
from base.global_config import SM__BUS_NAME, SM__OBJECT_PATH


print('start access.dbus')
print('use session.')
session_bus = SessionBus()
print('current bus_name: ', SM__BUS_NAME)
sm = session_bus.get(SM__BUS_NAME, SM__OBJECT_PATH)


def cb_signal_sm_service_changed(s_type, service_bus_name, service_obj_path, change_type, new_type):
    print(s_type, service_bus_name, service_obj_path, change_type, new_type)


def cb_signal_sm(*args):
    print(args)


def init():

    # session_bus.subscribe(object=SM__OBJECT_PATH,
    #                       signal_fired=cb_signal_sm)

    sm.ServicesChanged.connect(cb_signal_sm_service_changed)

    # ret = sm.ServicesRegister(
    #     "type0", "com.HACGI.example", "/com/HACGI/example")

    # ret = sm.ServicesDeleter("/com/HACGI/example")
